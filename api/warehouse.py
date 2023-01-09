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

class Almacen(BaseModel):
    id_alm: str
    temperatura: float
    superficie: float
    dni_super: Union[str, None] = None

class AlmacenUpdate(BaseModel):
    temperatura: Union[float, None] = None
    superficie: Union[float, None] = None
    dni_super: Union[str, None] = None

@router.get("/warehouse/", tags=["warehouse"])
def get_warehouses() -> List[Almacen]:
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        SELECT *
        FROM Almacen
        LIMIT 20;
        """
        cur.execute(statement)
        result = cur.fetchall()

        cur.close()
        # return a json with the result of the query
        warehouse = [dict((cur.description[i][0], value)
                         for i, value in enumerate(row)) for row in result]
        return warehouse
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail=f"Error en lectura de almacenes: {e.pgerror}")
    finally:
        if conn is not None:
            conn.close()

@router.get("/warehouse/{warehouse_id}/", tags=["warehouse"])
def get_warehouse(warehouse_id: str) -> Almacen:
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        SELECT *
        FROM Almacen 
        WHERE ID_ALM = %s;
        """
        cur.execute(statement, [warehouse_id])
        result = cur.fetchall()

        # Check whether it is a valid warehouse id or not.
        if not result:
            raise ValueError()
        warehouse = result[0]

        cur.close()
        # return a json with the result of the query
        return {cur.description[i][0]: value for i, value in enumerate(warehouse)}
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Almacen {warehouse_id} desconocido")
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail=f"Error en lectura de almacenes: {e.pgerror}")
    finally:
        if conn is not None:
            conn.close()

@router.post("/warehouse/", tags=["warehouse"])
def create_warehouse(new_warehouse: Almacen):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        INSERT INTO Almacen
        VALUES (%s, %s, %s, %s);
        """
        elements = [
            new_warehouse.id_alm,
            new_warehouse.temperatura,
            new_warehouse.superficie,
            new_warehouse.dni_super
        ]
        cur.execute(statement, elements)
        conn.commit()
        cur.close()
        return {"Insertada correctamente": {"id": new_warehouse.id_alm}}
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error en la inserción de almacenes: {e.pgerror}"
        )
    finally:
        if conn is not None:
            conn.close()

@router.put("/warehouse/{warehouse_id}/", tags=["warehouse"])
def update_warehouse(warehouse_id: str, updated_warehouse: AlmacenUpdate):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        SELECT Temperatura, Superficie, DNI_SUPER
        FROM Almacen 
        WHERE ID_ALM = %s;
        """
        cur.execute(statement, [warehouse_id])
        result = cur.fetchall()

        # Check whether it is a valid warehouse id or not.
        if not result:
            raise ValueError()
        
        # get the previous values
        warehouse = list(result[0])

        # update only the fields that are not None
        if updated_warehouse.temperatura is not None:
            warehouse[0] = updated_warehouse.temperatura
        if updated_warehouse.superficie is not None:
            warehouse[1] = updated_warehouse.superficie
        if updated_warehouse.dni_super is not None:
            warehouse[2] = updated_warehouse.dni_super

        # update the product
        statement = """
        UPDATE Almacen
        SET Temperatura = %s, Superficie = %s, DNI_SUPER = %s
        WHERE ID_ALM = %s;
        """
        cur.execute(statement, warehouse + [warehouse_id])
        conn.commit()
        cur.close()
        return {"Actualizado correctamente": {"id": warehouse_id}}
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Almacen {warehouse_id} desconocido")
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en la actualización de almacenes: {e.pgerror}"
        )
    finally:
        if conn is not None:
            conn.close()

@router.delete("/warehouse/{warehouse_id}/", tags=["warehouse"])
def delete_warehouse(warehouse_id: str):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        DELETE FROM Almacen
        WHERE ID_ALM = %s;
        """
        cur.execute(statement, [warehouse_id])
        conn.commit()
        cur.close()
        return {"Eliminada correctamente": {"id": warehouse_id}}
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error en la eliminación de almacenes: {e.pgerror}"
        )
    finally:
        if conn is not None:
            conn.close()
