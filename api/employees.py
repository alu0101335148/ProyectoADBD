from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from enum import Enum
from typing import Union, List
from datetime import date, time, datetime
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )
    return conn

router = APIRouter()

class Puesto(Enum):
    CAJERO = "Cajero"
    CHARCUTERIA = "Charcuteria"
    LOGISTICA = "Logistica"
    GERENTE = "Gerente"
    PESCADERIA = "Pescaderia"
    CARNICERIA = "Carniceria"

class Empleado(BaseModel):
    dni_emp: str
    nombre: str
    apellidos: str
    calle: str
    ciudad: str
    provincia: str
    salario: float
    horaentrada: time
    horasalida: time
    numcuenta: str
    rol: Puesto
    herramienta: Union[int, None] = None

class EmpleadoUpdate(BaseModel):
    nombre: Union[str, None] = None
    apellidos: Union[str, None] = None
    calle: Union[str, None] = None
    ciudad: Union[str, None] = None
    provincia: Union[str, None] = None
    salario: Union[float, None] = None
    horaentrada: Union[time, None] = None
    horasalida: Union[time, None] = None
    numcuenta: Union[str, None] = None
    rol: Union[Puesto, None] = None
    herramienta: Union[int, None] = None

MACHINES = {
    Puesto.CAJERO: "Caja",
    Puesto.CHARCUTERIA: "Cortadora",
    Puesto.LOGISTICA: "Montacargas",
}

@router.get("/employees/", tags=["employees"])
def get_employees() -> List[Empleado]:
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        SELECT *
        FROM Empleado
        LIMIT 20;
        """
        cur.execute(statement)
        result = cur.fetchall()

        # return a json with the result of the query
        employees = [dict((cur.description[i][0], value)
                     for i, value in enumerate(row)) for row in result]
        for employee in employees:
            rol = Puesto(employee["rol"])
            if rol in MACHINES.keys():
                table = rol.value
                statement = f"""
                SELECT {MACHINES[rol]}
                FROM {table}
                WHERE DNI_EMP = %s;
                """
                cur.execute(statement, [employee["dni_emp"]])
                result = cur.fetchall()
                employee["herramienta"] = result[0][0]
        cur.close()
        return employees
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail="Error en lectura de empleados")
    finally:
        if conn is not None:
            conn.close()

@router.get("/employees/{dni_emp}/", tags=["employees"])
def get_employee(dni_emp: str) -> Empleado:
    conn = None
    try:
        # Get the employee
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        SELECT *
        FROM Empleado 
        WHERE DNI_EMP = %s;
        """
        cur.execute(statement, [dni_emp])
        result = cur.fetchall()

        # Check whether it is a valid store id or not.
        if len(result) == 0:
            raise ValueError

        # return a json with the result of the query
        employee = dict((cur.description[i][0], value) for i, value in enumerate(result[0]))

        # Add the machine to the employee if it has one
        rol = Puesto(employee["rol"])
        if rol in MACHINES.keys():
            table = rol.value
            statement = f"""
            SELECT {MACHINES[rol]}
            FROM {table}
            WHERE DNI_EMP = %s;
            """
            cur.execute(statement, [dni_emp])
            result = cur.fetchall()
            employee["herramienta"] = result[0][0]

        cur.close()
        # return a json with the result of the query
        return employee
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Empleado/a {dni_emp} desconocido/a")
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail="Error en lectura de empleados")
    finally:
        if conn is not None:
            conn.close()

@router.post("/employees/", status_code=201, tags=["employees"])
def create_employee(employee: Empleado):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        INSERT INTO Empleado
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cur.execute(
            statement, 
            [
                employee.dni_emp, 
                employee.nombre, 
                employee.apellidos, 
                employee.calle, 
                employee.ciudad, 
                employee.provincia, 
                employee.salario, 
                employee.horaentrada, 
                employee.horasalida, 
                employee.numcuenta, 
                employee.rol.value
            ]
        )
        # insert the machine if it has one in the corresponding table
        rol = Puesto(employee.rol)
        if rol in MACHINES.keys():
            table = rol.value
            statement = f"""
            INSERT INTO {table} (DNI_EMP, {MACHINES[rol]})
            VALUES (%s, %s);
            """
            cur.execute(statement, [employee.dni_emp, employee.herramienta])
        conn.commit()
        cur.close()
        return {"Creado correctamente": employee.dict()}
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail="Error en creación de empleado/a")
    finally:
        if conn is not None:
            conn.close()

@router.put("/employees/{dni_emp}/", tags=["employees"])
def update_employee(dni_emp: str, employee: EmpleadoUpdate):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # get the previous information of the employee and update only the new information
        statement = """
        SELECT *
        FROM Empleado
        WHERE DNI_EMP = %s;
        """
        cur.execute(statement, [dni_emp])
        result = cur.fetchall()
        if len(result) == 0:
            raise ValueError
        previous_employee = dict((cur.description[i][0], value) for i, value in enumerate(result[0]))
        # update the employee with the new information 
        statement = """
        UPDATE Empleado
        SET nombre = %s, apellidos = %s, calle = %s, ciudad = %s, provincia = %s, salario = %s, horaentrada = %s, horasalida = %s, numcuenta = %s, rol = %s
        WHERE DNI_EMP = %s;
        """
        cur.execute(
            statement, 
            [
                employee.nombre or previous_employee["nombre"], 
                employee.apellidos or previous_employee["apellidos"], 
                employee.calle or previous_employee["calle"], 
                employee.ciudad or previous_employee["ciudad"], 
                employee.provincia or previous_employee["provincia"], 
                employee.salario or previous_employee["salario"], 
                employee.horaentrada or previous_employee["horaentrada"], 
                employee.horasalida or previous_employee["horasalida"], 
                employee.numcuenta or previous_employee["numcuenta"], 
                employee.rol.value or previous_employee["rol"], 
                dni_emp
            ]
        )
        # if the previous employee has a machine but with the new information not, then delete the entry in the corresponding table
        if previous_employee["rol"] in MACHINES.keys() and employee.rol not in MACHINES.keys():
            table = previous_employee["rol"].value
            statement = f"""
            DELETE FROM {table}
            WHERE DNI_EMP = %s;
            """
            cur.execute(statement, [dni_emp])
        # if the previous employee has a machine and with the new information also, but in a different role, then delete the previous entry and insert the new one
        elif previous_employee["rol"] in MACHINES.keys() and employee.rol and previous_employee["rol"] != employee.rol.value:
            table = previous_employee["rol"].value
            statement = f"""
            DELETE FROM {table}
            WHERE DNI_EMP = %s;
            """
            cur.execute(statement, [dni_emp])
            table = employee.rol.value
            statement = f"""
            INSERT INTO {table} (DNI_EMP, {MACHINES[employee.rol]})
            VALUES (%s, %s);
            """
            cur.execute(statement, [dni_emp, employee.herramienta])
        # if the previous employee has a machine and with the new information also, but in the same role, then update the machine
        elif previous_employee["rol"] in MACHINES.keys() and employee.rol:
            table = previous_employee["rol"].value
            statement = f"""
            UPDATE {table}
            SET {MACHINES[previous_employee["rol"]]} = %s
            WHERE DNI_EMP = %s;
            """
            cur.execute(statement, [employee.herramienta, dni_emp])
        # if the previous employee has not a machine but with the new information yes, then insert the new one
        elif previous_employee["rol"] not in MACHINES.keys() and employee.rol:
            table = employee.rol.value
            statement = f"""
            INSERT INTO {table} (DNI_EMP, {MACHINES[employee.rol]})
            VALUES (%s, %s);
            """
            cur.execute(statement, [dni_emp, employee.herramienta])
        conn.commit()
        cur.close()
        return {"Actualizado correctamente": employee.dict()}
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Empleado/a {dni_emp} desconocido/a")
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail="Error en actualización de empleado/a")
    finally:
        if conn is not None:
            conn.close()

@router.delete("/employees/{dni_emp}/", tags=["employees"])
def delete_employee(dni_emp: str):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        DELETE FROM Empleado
        WHERE dni_emp = %s;
        """
        cur.execute(statement, [dni_emp])
        # delete the machine if it has one in the corresponding table
        statement = """
        SELECT rol
        FROM Empleado
        WHERE dni_emp = %s;
        """
        cur.execute(statement, [dni_emp])
        result = cur.fetchall()
        if len(result) != 0:
            rol = Puesto(result[0][0])
            if rol in MACHINES.keys():
                table = rol.value
                statement = f"""
                DELETE FROM {table}
                WHERE DNI_EMP = %s;
                """
                cur.execute(statement, [dni_emp])
        conn.commit()
        cur.close()
        return {"Borrado correctamente": dni_emp}
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail="Error en borrado de empleado/a")
    finally:
        if conn is not None:
            conn.close()
