import asyncio
import json
from pathlib import Path
import re
from fastmcp import Client
from hr_llm_invoke import call_bcai_llm, generate_response
 
 
async def main():
 
    user_question = input("Ask your question: ")
 
    with open(
        "prompts.txt",
        "r",
        encoding="utf-8"
    ) as f:
        system_prompt = f.read()
 
    prompt = f"""
User Question: {user_question}
 
Available Tools:
 
1. get_employee_by_id(employee_id)
2. search_employee_by_name(name)
3. get_employees_by_department_id(department_id)
4. get_employees_by_department_name(department_name)
 
Return ONLY valid JSON.
 
Examples:
 
{{"tool":"search_employee_by_name","value":"Steven"}}
 
{{"tool":"get_employee_by_id","value":"100"}}
 
{{"tool":"get_employees_by_department_name","value":"IT"}}

Rules:
- If the user asks about employee data, select a tool.
- If no tool is required, return tool as "none"
  and provide a direct response in value.
- For greetings or general questions, do not call a tool.
"""
 
    response = call_bcai_llm(
        system_prompt,
        prompt
    )
    # print("LLM Response: before json loadas", response)

    response = json.loads(response)

    # print("LLM Response:", type(response))
 
    routing = response
 
    tool_name = routing["tool"]
    value = routing["value"]
 
    async with Client(Path("local_server.py")) as client:
 
        if tool_name == "search_employee_by_name":
 
            result = await client.call_tool(
                tool_name,
                {"name": value}
            )
 
        elif tool_name == "get_employee_by_id":
 
            result = await client.call_tool(
                tool_name,
                {"employee_id": int(value)}
            )
 
        elif tool_name == "get_employees_by_department_id":
 
            result = await client.call_tool(
                tool_name,
                {"department_id": int(value)}
            )
 
        elif tool_name == "get_employees_by_department_name":
 
            result = await client.call_tool(
                tool_name,
                {"department_name": value}
            )

        elif tool_name == "none":
            print(f"Assistant: ",value)
            return
           
 
        else:
 
            raise ValueError(
                f"Unknown tool: {tool_name}"
            )
 
    # print("\nResult:")
 
 
    print(result)
 
    user_prompt = f"""
User Question:
{user_question}
 
Employee Data:
{result.content[0].text}
 
Please answer the user's question using only the employee data provided.
 
Requirements:
- Use simple business English.
- Provide a direct answer.
- If multiple employees match, list each employee separately.
- Include employee name and relevant details requested by the user.
- If the user asks about salary, mention the salary.
- If the user asks about department, mention the department.
- If the user asks about manager, mention the manager id.
- Do not mention JSON, SQL, database tables, MCP, tools, or technical details.
- If no records are found, clearly state that no matching employee was found.
 
Answer:
"""
 
   
 
   
    response = generate_response(user_prompt)
 
    print(response)
 
 
if __name__ == "__main__":
    asyncio.run(main())
 
 