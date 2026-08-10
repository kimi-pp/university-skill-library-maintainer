#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const DEFAULT_PORT = process.env.CDP_PORT || "9222";
const DEFAULT_BASE = `http://127.0.0.1:${DEFAULT_PORT}`;

function usage() {
  console.log(`UCAS course evaluation CDP helper

Commands:
  status
  navigate --portal-url <url>
  collect --out <raw.json>
  draft --raw <raw.json> --out <draft.json> --preview <preview.md> [--quick-positive] [--comments <comments.json>]
  submit --draft <draft.json> --i-understand-submit-is-final
  verify

Environment:
  CDP_PORT=9222

Notes:
  - Run from a scratch workspace, not from inside the skill folder.
  - Launch Chrome with --remote-debugging-port before using this helper.
  - Do not run submit until the user has explicitly confirmed final submission.
`);
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith("--")) {
      args._.push(arg);
    } else {
      const key = arg.slice(2);
      const next = argv[i + 1];
      if (!next || next.startsWith("--")) {
        args[key] = true;
      } else {
        args[key] = next;
        i += 1;
      }
    }
  }
  return args;
}

function ensureParent(filePath) {
  const dir = path.dirname(path.resolve(filePath));
  fs.mkdirSync(dir, { recursive: true });
}

async function getJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}: ${url}`);
  return res.json();
}

async function listTabs(base = DEFAULT_BASE) {
  return (await getJson(`${base}/json`)).filter((tab) => tab.type === "page");
}

async function getTab(preferBkk = false) {
  const tabs = await listTabs();
  if (!tabs.length) throw new Error("No Chrome page tabs found on the CDP port.");
  return (
    (preferBkk && tabs.find((tab) => tab.url.includes("bkkcpj.ucas.ac.cn"))) ||
    tabs.find((tab) => tab.url.includes("sep.ucas.ac.cn")) ||
    tabs[0]
  );
}

class CDP {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.ws = null;
    this.id = 0;
    this.pending = new Map();
  }

  async open() {
    this.ws = new WebSocket(this.wsUrl);
    this.ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && this.pending.has(msg.id)) {
        this.pending.get(msg.id)(msg);
        this.pending.delete(msg.id);
      }
    };
    await new Promise((resolve, reject) => {
      this.ws.onopen = resolve;
      this.ws.onerror = reject;
    });
  }

  send(method, params = {}) {
    const id = ++this.id;
    this.ws.send(JSON.stringify({ id, method, params }));
    return new Promise((resolve) => this.pending.set(id, resolve));
  }

  async eval(expression, timeoutMs = 30000) {
    const timer = new Promise((_, reject) =>
      setTimeout(() => reject(new Error(`Runtime.evaluate timeout after ${timeoutMs} ms`)), timeoutMs)
    );
    const result = await Promise.race([
      this.send("Runtime.evaluate", {
        expression,
        awaitPromise: true,
        returnByValue: true,
      }),
      timer,
    ]);
    if (result.error) throw new Error(JSON.stringify(result.error));
    if (result.result?.exceptionDetails) {
      throw new Error(result.result.exceptionDetails.text || "Runtime exception");
    }
    return result.result.result.value;
  }

  close() {
    if (this.ws) this.ws.close();
  }
}

async function withTab(fn, preferBkk = false) {
  const tab = await getTab(preferBkk);
  const cdp = new CDP(tab.webSocketDebuggerUrl);
  await cdp.open();
  try {
    await cdp.send("Page.enable");
    await cdp.send("Runtime.enable");
    return await fn(cdp, tab);
  } finally {
    cdp.close();
  }
}

function parseEvalJson(value) {
  return typeof value === "string" ? JSON.parse(value) : value;
}

async function status() {
  const tabs = await listTabs();
  console.log(
    JSON.stringify(
      tabs.map((tab) => ({
        id: tab.id,
        title: tab.title,
        url: tab.url,
      })),
      null,
      2
    )
  );
}

async function navigate(args) {
  const portalUrl = args["portal-url"] || process.env.UCAS_EVAL_PORTAL_URL;
  if (!portalUrl) throw new Error("Missing --portal-url or UCAS_EVAL_PORTAL_URL.");
  await withTab(async (cdp) => {
    await cdp.send("Page.navigate", { url: portalUrl });
    const started = Date.now();
    while (Date.now() - started < 45000) {
      await new Promise((resolve) => setTimeout(resolve, 1000));
      const tabs = await listTabs();
      const bkk = tabs.find((tab) => tab.url.includes("bkkcpj.ucas.ac.cn"));
      if (bkk) {
        console.log(JSON.stringify({ title: bkk.title, url: bkk.url }, null, 2));
        return;
      }
    }
    const info = await cdp.eval(`JSON.stringify({ title: document.title, url: location.href })`);
    console.log(info);
  });
}

async function collect(args) {
  const out = args.out || "work/ucas-eval-raw.json";
  const raw = await withTab(
    async (cdp) =>
      parseEvalJson(
        await cdp.eval(`(async () => {
          const request = async (url, opts = {}) => {
            const res = await fetch(url, { credentials: "include", ...opts });
            const text = await res.text();
            let body;
            try { body = JSON.parse(text); } catch { body = text.slice(0, 500); }
            return { ok: res.ok, status: res.status, url: res.url, body };
          };
          const termsRes = await request("/ea00031/findAllTerms");
          const terms = termsRes.body.data || termsRes.body || [];
          const term = terms.find((item) => item.selected) || terms[0];
          if (!term) throw new Error("No term returned from findAllTerms.");
          const params = new URLSearchParams({
            title: "",
            pollTypeId: "",
            type: "",
            termId: String(term.id)
          });
          const coursesRes = await request("/myCourse/list?" + params.toString(), { method: "POST" });
          const courses = coursesRes.body.data || coursesRes.body || [];
          const forms = [];
          for (const course of courses) {
            if (course.voted) continue;
            const p = new URLSearchParams({ id: String(course.pollId), courseId: String(course.courseId) });
            const detailRes = await request("/myPoll/getById?" + p.toString());
            forms.push({ course, detail: detailRes.body });
          }
          return JSON.stringify({ location: location.href, term, courses, forms });
        })()`, 120000)
      ),
    true
  );
  ensureParent(out);
  fs.writeFileSync(out, JSON.stringify(raw, null, 2), "utf8");
  console.log(
    JSON.stringify(
      {
        out,
        term: raw.term?.name,
        courseCount: raw.courses?.length || 0,
        unfilledCount: raw.forms?.length || 0,
        courses: (raw.courses || []).map((course) => ({
          courseName: course.courseName,
          instructors: course.instructors,
          statusName: course.statusName,
          voted: course.voted,
          pollId: course.pollId,
          courseId: course.courseId,
        })),
      },
      null,
      2
    )
  );
}

function loadComments(filePath) {
  if (!filePath) return {};
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function optionValues(question) {
  return (question.options2 || []).map((option) => String(option.value ?? option.label ?? "")).filter(Boolean);
}

function pickPositive(question, quickPositive, warnings, courseName) {
  const values = optionValues(question);
  const title = question.title || "";
  if (/是否有助教/.test(title) && !quickPositive) {
    warnings.push(`${courseName} ${question.seq}: factual TA question needs user/course evidence.`);
    return "";
  }
  if (/课后投入|学习.*时间/.test(title) && !quickPositive) {
    warnings.push(`${courseName} ${question.seq}: time-investment question needs user preference.`);
    return "";
  }
  const preferred = ["非常符合", "非常同意", "非常满意", "超过4小时", "有助教", "会", "优秀", "很好", "好", "满意", "是", "5", "10"];
  for (const word of preferred) {
    const hit = values.find((value) => value.includes(word));
    if (hit) return hit;
  }
  return values[0] || "";
}

function courseText(courseName, title, comments) {
  const custom = comments[courseName] || {};
  if (/助教/.test(title)) return custom.ta || "助教能够及时协助答疑和反馈，整体认真负责。建议继续保持课后沟通渠道畅通。";
  if (/希望.*领域|哪个领域/.test(title)) return custom.topic || "人工智能、科技创新、交叉学科与社会发展相关主题。";
  if (/哪场|印象深刻/.test(title)) {
    return custom.lecture || "本学期关于前沿科学进展与现实问题的讲座给我印象较深，内容开阔且有启发。";
  }
  if (/改进|建议|意见|不足|希望/.test(title)) {
    return custom.advice || "建议继续增加案例讲解、课堂互动和阶段性总结，帮助同学更好地理解重点内容。";
  }
  const summary = custom.summary || `课程内容安排较为合理，${courseName}的重点讲解清楚，对理解相关知识和提升综合能力有帮助。`;
  const advice = custom.advice || "建议继续增加案例讲解、课堂互动和阶段性总结。";
  return /整体感受/.test(title) ? `${summary}${advice}` : summary;
}

function clearCustom(question) {
  if (question.answer2 !== undefined) question.answer2 = "";
  for (const row of question.options || []) {
    if (row.answer2 !== undefined) row.answer2 = "";
  }
}

function fillQuestion(question, courseName, comments, quickPositive, warnings) {
  clearCustom(question);
  const type = String(question.type);
  if (type === "1" || type === "4") {
    question.answer = pickPositive(question, quickPositive, warnings, courseName);
  } else if (type === "2") {
    const answer = pickPositive(question, quickPositive, warnings, courseName);
    question.answers = answer ? [answer] : [];
  } else if (type === "3") {
    question.answer = courseText(courseName, question.title || "", comments);
  } else if (type === "5" || type === "6") {
    const answer = pickPositive(question, quickPositive, warnings, courseName);
    for (const row of question.options || []) row.answer = answer;
  } else if (type === "7") {
    const answer = pickPositive(question, quickPositive, warnings, courseName);
    for (const row of question.options || []) row.answers = answer ? [answer] : [];
  }
}

function validateDraft(drafts) {
  const issues = [];
  for (const { course, form } of drafts) {
    for (const question of form.questions || []) {
      const type = String(question.type);
      if (!question.requiredAnswer) continue;
      if ((type === "1" || type === "4") && !question.answer) issues.push(`${course.courseName} ${question.seq}: missing answer`);
      if (type === "2" && (!question.answers || !question.answers.length)) issues.push(`${course.courseName} ${question.seq}: missing answers`);
      if (type === "3" && !String(question.answer || "").trim()) issues.push(`${course.courseName} ${question.seq}: missing text`);
      if ((type === "5" || type === "6")) {
        for (const [idx, row] of (question.options || []).entries()) {
          if (!row.answer) issues.push(`${course.courseName} ${question.seq}.${idx}: missing matrix answer`);
        }
      }
      if (type === "7") {
        for (const [idx, row] of (question.options || []).entries()) {
          if (!row.answers || !row.answers.length) issues.push(`${course.courseName} ${question.seq}.${idx}: missing matrix answers`);
        }
      }
    }
  }
  return issues;
}

async function draft(args) {
  const rawPath = args.raw || "work/ucas-eval-raw.json";
  const out = args.out || "work/ucas-eval-draft.json";
  const preview = args.preview || "outputs/course_eval_preview.md";
  const comments = loadComments(args.comments);
  const quickPositive = Boolean(args["quick-positive"]);
  const raw = JSON.parse(fs.readFileSync(rawPath, "utf8"));
  const warnings = [];
  const drafts = [];

  for (const item of raw.forms || []) {
    const form = item.detail.data || item.detail;
    form.courseId = String(item.course.courseId);
    for (const question of form.questions || []) {
      fillQuestion(question, item.course.courseName, comments, quickPositive, warnings);
    }
    drafts.push({ course: item.course, form });
  }

  const issues = validateDraft(drafts);
  ensureParent(out);
  fs.writeFileSync(out, JSON.stringify({ createdAt: new Date().toISOString(), quickPositive, warnings, issues, drafts }, null, 2), "utf8");

  const lines = [];
  lines.push("# UCAS Course Evaluation Preview", "");
  lines.push(`Term: ${raw.term?.name || ""}`);
  lines.push(`Draft count: ${drafts.length}`);
  lines.push(`Policy: ${quickPositive ? "quick-positive selections plus generated text" : "generated draft with factual warnings"}`, "");
  if (warnings.length) lines.push("## Warnings", "", ...warnings.map((item) => `- ${item}`), "");
  if (issues.length) lines.push("## Required Blanks", "", ...issues.map((item) => `- ${item}`), "");
  for (const { course, form } of drafts) {
    lines.push(`## ${course.courseName}`, "");
    lines.push(`- Instructors: ${course.instructors || ""}`);
    lines.push(`- Poll: ${form.title || course.pollId}`);
    for (const question of form.questions || []) {
      if (String(question.type) === "3") lines.push(`- ${question.seq}. ${question.title}: ${question.answer || ""}`);
    }
    lines.push("");
  }
  ensureParent(preview);
  fs.writeFileSync(preview, lines.join("\n"), "utf8");
  console.log(JSON.stringify({ out, preview, draftCount: drafts.length, warnings, issues }, null, 2));
}

async function submit(args) {
  if (!args["i-understand-submit-is-final"]) {
    throw new Error("Refusing to submit without --i-understand-submit-is-final.");
  }
  const draftPath = args.draft || "work/ucas-eval-draft.json";
  const saved = JSON.parse(fs.readFileSync(draftPath, "utf8"));
  if (saved.issues && saved.issues.length) throw new Error(`Draft has required blanks: ${saved.issues.join("; ")}`);
  const drafts = saved.drafts || [];
  const result = await withTab(
    async (cdp) =>
      parseEvalJson(
        await cdp.eval(`(async () => {
          const drafts = ${JSON.stringify(drafts)};
          const results = [];
          for (const item of drafts) {
            const res = await fetch("/myPoll/submit", {
              method: "POST",
              credentials: "include",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(item.form)
            });
            const text = await res.text();
            let body;
            try { body = JSON.parse(text); } catch { body = text.slice(0, 500); }
            results.push({
              courseName: item.course.courseName,
              status: res.status,
              ok: res.ok,
              code: body && body.code,
              message: body && body.message
            });
            await new Promise((resolve) => setTimeout(resolve, 500));
          }
          return JSON.stringify(results);
        })()`, 120000)
      ),
    true
  );
  console.log(JSON.stringify(result, null, 2));
}

async function verify() {
  await collect({ out: "work/ucas-eval-verify.json" });
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const cmd = args._[0];
  if (!cmd || cmd === "help" || cmd === "--help" || cmd === "-h") return usage();
  if (cmd === "status") return status(args);
  if (cmd === "navigate") return navigate(args);
  if (cmd === "collect") return collect(args);
  if (cmd === "draft") return draft(args);
  if (cmd === "submit") return submit(args);
  if (cmd === "verify") return verify(args);
  throw new Error(`Unknown command: ${cmd}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error.stack || error.message || String(error));
    process.exit(1);
  });
