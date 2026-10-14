import oracledb as db
 
 
def getConnectionObj():
    return db.connect(
        user="hr",
        password="hr",
        host="localhost",
        port=1521,
        service_name="xepdb1"
    )
 
 
def _fetch_as_dict(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
 
 
def get_employee_by_id(employee_id: int):
    with getConnectionObj() as conn:
        cursor = conn.cursor()
 
        cursor.execute("""
            SELECT *
            FROM EMPLOYEES
            WHERE EMPLOYEE_ID = :employee_id
        """, employee_id=employee_id)
 
        return _fetch_as_dict(cursor)
 
 
def search_employee_by_name(name: str):
    with getConnectionObj() as conn:
        cursor = conn.cursor()
 
        cursor.execute("""
            SELECT *
            FROM EMPLOYEES
            WHERE UPPER(FIRST_NAME) LIKE UPPER(:name)
               OR UPPER(LAST_NAME)  LIKE UPPER(:name)
        """, name=f"%{name}%")
 
        return _fetch_as_dict(cursor)
 
 
def get_employees_by_department_id(department_id: int):
    with getConnectionObj() as conn:
        cursor = conn.cursor()
 
        cursor.execute("""
            SELECT *
            FROM EMPLOYEES
            WHERE DEPARTMENT_ID = :department_id
        """, department_id=department_id)
 
        return _fetch_as_dict(cursor)
 
def get_employees_by_department_name(department_name: str):
    with getConnectionObj() as conn:
        cursor = conn.cursor()
 
        cursor.execute("""
            SELECT e.*
            FROM EMPLOYEES e
                 JOIN DEPARTMENTS d
                   ON e.DEPARTMENT_ID = d.DEPARTMENT_ID
            WHERE UPPER(d.DEPARTMENT_NAME)
                  LIKE UPPER(:department_name)
        """, department_name=f"%{department_name}%")
 
        return _fetch_as_dict(cursor)
 