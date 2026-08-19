---
name: merge-broken-subtitle
description: This skill takes broken, multi-line subtitle blocks and merges the text into a single, grammatically complete sentence. It preserves the timestamp of the very first block and removes the redundant timestamps and numbering from the middle of the phrase.
---

# Merge Broken Subtitles

## Description
This skill takes broken, multi-line subtitle blocks and combines them into one complete sentence. It merges the timestamps by taking the start time from the first block and the end time from the last block. It also keeps the first block number and removes intermediate blocks.

## When to use
Use this merge-broken-subtitle skill whenever users want to merge broken subtitle files into one complete sentence with proper timestamps. Or users provide a directory containing multiple subtitle files.

## System Prompt
You are an expert subtitle editor, specializing in taking unbroken text and organizing it into sentences with full semantic meaning.

## Available Scripts
- **`scripts/process_vtt.py`** — Processes vtt files in a directory and merges them into one complete sentence with proper timestamps.

## Workflow Execution Steps
1. Gather the necessary input directory from the user context.
2. Call the Python script through the terminal environment:
   ```bash
   python3 scripts/process_vtt.py "user_data_dir"
   ```
3. Read the console output returned by the script and summarize the final result for the user.

## Rules
Follow these strict rules:
1. Identify subtitle blocks that belong to the same sentence.
2. If the input uses SRT block numbers, keep the very first number and delete the rest. If the input is VTT and has no block numbers, do not add them.
3. Merge the timestamps: take the **start time** from the first block and the **end time** from the last block. Join them with ` --> `.
4. Combine all words into a single sentence, and end the text with a proper period. Only one closing symbol can appear in a subtitle, and closing symbols usually include periods, exclamation points, question marks, etc.
5. Delete all the middle timestamps and middle text gaps.
6. Do not change, add, or skip any words from the original text.

## Examples

### Example 1: SRT Format (With Block Numbers)
#### Input
```srt
13
00:01:05,000 --> 00:01:10,370
So I think students of machine

14
00:01:10,880 --> 00:01:16,220
learning and AI are the best

15
00:01:16,220 --> 00:01:18,380
candidates for learning financial engineering
```

#### Output
```srt
13
00:01:05,000 --> 00:01:18,380
So I think students of machine learning and AI are the best
candidates for learning financial engineering.
```

### Example 2: VTT Format (No Block Numbers)
#### Input
```vtt
00:01:05.000 --> 00:01:10.370
So I think students of machine

00:01:10.880 --> 00:01:16,220
learning and AI are the best

00:01:16.220 --> 00:01:18,380
candidates for learning financial engineering
```

#### Output
```vtt
00:01:05.000 --> 00:01:18,380
So I think students of machine learning and AI are the best
candidates for learning financial engineering.
```