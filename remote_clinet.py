
import asyncio
import json
from fastmcp import Client
from hr_llm_invoke import call_bcai_llm, generate_response


async def main():

    user_question = input("Ask your question: ")

    with open("prompts.txt", "r", encoding="utf-8") as f:
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
- Employee data question: select the correct tool.
- Greeting or general question: use tool "none".
- For tool "none", put the direct answer in value.
"""

    # Get tool selection from LLM (retry up to 3 times)
    routing = None

    for attempt in range(3):
        try:
            response = call_bcai_llm(system_prompt, prompt)
            print("LLM response:", response)

            routing = json.loads(response)

            if isinstance(routing, dict) and "tool" in routing and "value" in routing:
                break

            routing = None

        except (json.JSONDecodeError, TypeError):
            routing = None

        print(f"Attempt {attempt + 1} failed.")

    if routing is None:
        print("LLM failed to return valid JSON. Please try again.")
        return

    tool_name = routing["tool"]
    value = routing["value"]

    # Handle general questions without calling MCP
    if tool_name == "none":
        print("Assistant:", value)
        return

    # Connect to the REMOTE MCP server
    async with Client("http://localhost:8000/mcp") as client:

        if tool_name == "search_employee_by_name":
            result = await client.call_tool(
                tool_name, {"name": value}
            )

        elif tool_name == "get_employee_by_id":
            result = await client.call_tool(
                tool_name, {"employee_id": int(value)}
            )

        elif tool_name == "get_employees_by_department_id":
            result = await client.call_tool(
                tool_name, {"department_id": int(value)}
            )

        elif tool_name == "get_employees_by_department_name":
            result = await client.call_tool(
                tool_name, {"department_name": value}
            )

        else:
            print("Unknown tool:", tool_name)
            return

    # Read MCP result safely
    if not result.content:
        print("MCP returned no data.")
        return

    employee_data = "\n".join(
        item.text for item in result.content
        if hasattr(item, "text") and item.text
    )

    if not employee_data:
        print("No readable employee data returned.")
        return

    # Ask LLM to explain the employee data
    user_prompt = f"""
User Question:
{user_question}

Employee Data:
{employee_data}

Answer using only the employee data.
Use simple business English and answer directly.
Do not invent information.
If no matching records exist, say so clearly.
"""

    response = generate_response(user_prompt)
    print("Assistant:", response)


if __name__ == "__main__":
    asyncio.run(main())
