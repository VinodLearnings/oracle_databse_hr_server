import os
import uuid
import json
import httpx

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import (HumanMessage,SystemMessage)
from IPython.display import Markdown, display
os.environ['HUGGINGFACEHUB_API_TOKEN']="===KEY==="
TIMEOUT_SECONDS = 60
repo_id="google/gemma-3-27b-it"

model_llm=HuggingFaceEndpoint(repo_id=repo_id,
                    task="generated_text")

chat_model= ChatHuggingFace(llm=model_llm)
 
 


def call_bcai_llm(system_prompt, user_prompt):
          message_lst=[
          SystemMessage(content=system_prompt),
          HumanMessage(content=user_prompt)        

                    ]
          response_model=chat_model.invoke(message_lst)          
          return response_model.content

 
 
 
 
 
 
 
def generate_response(user_prompt):
 
 system_prompt = """
 
            You are an HR assistant.
 
Your job is to answer the user's question using the employee data provided.
 
Rules:
- Use only the provided employee data.
- Answer in simple business English.
- If multiple employees are returned, clearly list each employee separately.
- Include relevant details such as employee name, salary, department id, job id, manager id when applicable.
- If no employee is found, clearly say no matching employee was found.
- Do not mention JSON, database records, MCP tools, SQL queries, or technical details.
- Provide a direct answer to the user's question.
 
            """
 
   
 message_lst=[
             SystemMessage(content=system_prompt),
             HumanMessage(content=user_prompt)        
   
                       ]
   
 response_model=chat_model.invoke(message_lst)
   
             
 return response_model.content
 