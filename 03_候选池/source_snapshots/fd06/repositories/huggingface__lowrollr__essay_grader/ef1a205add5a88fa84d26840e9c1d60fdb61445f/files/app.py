from typing import Dict
import gradio as gr
import openai
import os
import json

from langchain import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

MODEL = "gpt-3.5-turbo"

try:
    openai.api_key = os.getenv("OPENAI_API_KEY")
except:
    print("Set the OPENAI_API_KEY environment variable")
    exit()

with open('./rubrics/act_rubric.json', 'r') as j:
     act_rubric = json.loads(j.read())

class ScoreDescription(BaseModel):
    score: int = Field(description="The score given")
    description: str = Field(description="Why the score was given")

class ACTScore(BaseModel):
    sub_scores: Dict[str, ScoreDescription] = Field(description="The sub-scores of the essay for each category in the rubric")
    overall_feedback: str = Field(description="Overall feedback for the essay")

parser = PydanticOutputParser(pydantic_object=ACTScore)

grader_template = PromptTemplate(
    input_variables=['rubric', 'essay_prompt', 'essay'],
    template= """
        You are an essay grader provided with the following grading rubric:\n
        {rubric}
        \n
        The essay writer was given the following instructions to write the essay: \n
        {essay_prompt}
        \n
        Grade the following essay. Provide sub-scores and rationale for each sub-score. \n
        {essay}
        \n

        Format description:
        {format_description}
    """,
    partial_variables={
        'format_description': parser.get_format_instructions()
    }

)
    
def get_prompt(essay, essay_prompt):
    return grader_template.format(
        rubric=act_rubric,
        essay=essay,
        essay_prompt=essay_prompt
    )



def grade_essay(essay, essay_prompt):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role":"user", "content":get_prompt(essay, essay_prompt)}],
        temperature=0.0,
        max_tokens=1000,
    )
    
    result = response['choices'][0]['message']['content']
    return result

demo = gr.Interface(fn=grade_essay, inputs=[gr.Textbox(lines=10, placeholder='Essay'), gr.Textbox(lines=10, placeholder='Essay Prompt')], outputs="text")

demo.launch()



