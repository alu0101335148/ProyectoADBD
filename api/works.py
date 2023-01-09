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

class Trabaja(BaseModel):
    dni_emp: str
    id_tie: str
    fechainicio: date
    fechafin: Union[date, None] = None

@router.get("/works/", tags=["works"])
def get_works() -> List[Trabaja]:
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        SELECT *
        FROM Trabaja
        LIMIT 20;
        """
        cur.execute(statement)
        result = cur.fetchall()

        # return a json with the result of the query
        works = [dict((cur.description[i][0], value)
                         for i, value in enumerate(row)) for row in result]
        cur.close()
        return works
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail=f"Error en lectura de trabajos: {e.pgerror}")
    finally:
        if conn is not None:
            conn.close()


@router.get("/works/{dni_emp}/", tags=["works"])
def get_works_by_employee(dni_emp: str) -> List[Trabaja]:
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        SELECT *
        FROM Trabaja 
        WHERE DNI_EMP = %s;
        """
        cur.execute(statement, [dni_emp])
        result = cur.fetchall()

        # Check whether it is a valid store id or not.
        if not result:
            raise ValueError()
        works = result

        cur.close()
        # return a json with the result of the query
        return [dict((cur.description[i][0], value)
                         for i, value in enumerate(row)) for row in works]
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Trabajo de {dni_emp} desconocida")
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail=f"Error en lectura de trabajos: {e.pgerror}")
    finally:
        if conn is not None:
            conn.close()

@router.post("/works/", tags=["works"])
def create_work(work: Trabaja):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        INSERT INTO Trabaja
        VALUES (%s, %s, %s, %s);
        """
        cur.execute(statement, [work.dni_emp, work.id_tie, work.fechainicio, work.fechafin])
        conn.commit()
        cur.close()
        return {"Creado correctamente": work.dict()}
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail=f"Error en creación de trabajo: {e.pgerror}")
    finally:
        if conn is not None:
            conn.close()

@router.put("/works/finish/{dni_emp}/", tags=["works"])
def update_work(dni_emp: str):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        UPDATE Trabaja
        SET FechaFin = %s
        WHERE dni_emp = %s AND FechaFin IS NULL;
        """
        cur.execute(statement, [date.today(), dni_emp])
        conn.commit()
        cur.close()
        return {"Actualizado correctamente": dni_emp}
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail=f"Error en actualización de trabajo: {e.pgerror}")
    finally:
        if conn is not None:
            conn.close()    
