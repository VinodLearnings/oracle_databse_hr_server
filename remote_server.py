from fastmcp import FastMCP
 
from hr_db_tools import (
    get_employee_by_id as db_get_employee_by_id,
    search_employee_by_name as db_search_employee_by_name,
    get_employees_by_department_id as db_get_employees_by_department_id,
    get_employees_by_department_name as db_get_employees_by_department_name
)
 
mcp = FastMCP("employees")
 
 
@mcp.tool()
def get_employee_by_id(employee_id: int):
    """Get employee details by employee id."""
    return db_get_employee_by_id(employee_id)
 
 
@mcp.tool()
def search_employee_by_name(name: str):
    """Search employees by first name or last name."""
    return db_search_employee_by_name(name)
 
 
@mcp.tool()
def get_employees_by_department_id(department_id: int):
    """Get all employees belonging to a department id."""
    return db_get_employees_by_department_id(department_id)
 
 
@mcp.tool()
def get_employees_by_department_name(department_name: str):
    """Get all employees belonging to a department name."""
    return db_get_employees_by_department_name(department_name)
 
 
if __name__ == "__main__":
    mcp.run(transport="http",host="0.0.0.0",port=8000) # makingthe server in remote (internet)
 