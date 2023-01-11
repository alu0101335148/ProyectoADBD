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

class Destino(str, Enum):
    TIENDA = "Tienda"
    ALMACEN = "Almacen"

class DisponibilidadTienda(BaseModel):
    id_tie: str
    id_prod: int
    cantidad: int

class DisponibilidadAlmacen(BaseModel):
    id_alm: str
    id_prod: int
    cantidad: int

class DisponibilidadUpdate(BaseModel):
    id_prod: str
    cantidad: int

@router.get("/availability/", tags=["availability"])
def get_availability(destination: Destino) -> List[Union[DisponibilidadTienda, DisponibilidadAlmacen]]:
    conn = None
    try:
        if destination is Destino.TIENDA:
            table = "DisponibilidadTienda"
        elif destination is Destino.ALMACEN:
            table = "DisponibilidadAlmacen"

        conn = get_db_connection()
        cur = conn.cursor()
        statement = f"""
        SELECT * FROM {table}
        LIMIT 20
        """
        cur.execute(statement, [])
        result = cur.fetchall()
        cur.close()
        # return a json with the result of the query
        stock = [dict((cur.description[i][0], value)
                         for i, value in enumerate(row)) for row in result]
        return stock
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail="Error en lectura de stock")
    finally:
        if conn is not None:
            conn.close()

@router.get("/availability/{id}/", tags=["availability"])
def get_availability_by_id(destination: Destino, id: str) -> List[Union[DisponibilidadTienda, DisponibilidadAlmacen]]:
    conn = None
    try:
        if destination is Destino.TIENDA:
            table = "DisponibilidadTienda"
            id_name = "ID_TIE"
        elif destination is Destino.ALMACEN:
            table = "DisponibilidadAlmacen"
            id_name = "ID_ALM"
        conn = get_db_connection()
        cur = conn.cursor()
        statement = f"""
        SELECT * FROM {table}
        WHERE {id_name} = %s;
        """
        cur.execute(statement, [id])
        result = cur.fetchall()
        cur.close()

        # Check whether it is a valid warehouse id or not.
        if not result:
            raise ValueError()
        stock = result

        cur.close()
        # return a json with the result of the query
        stock = [dict((cur.description[i][0], value)
                         for i, value in enumerate(row)) for row in result]
        return stock
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"{destination.value} {id} desconocido/a")
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail="Error en lectura de stock")
    finally:
        if conn is not None:
            conn.close()

@router.post("/availability/", status_code=201, tags=["availability"])
def create_availability(destination: Destino, availability: Union[DisponibilidadTienda, DisponibilidadAlmacen]):
    conn = None
    try:
        if destination is Destino.TIENDA:
            table = "DisponibilidadTienda"
        elif destination is Destino.ALMACEN:
            table = "DisponibilidadAlmacen"

        conn = get_db_connection()
        cur = conn.cursor()
        statement = f"""
        INSERT INTO {table}
        VALUES (%s, %s, %s);
        """
        if isinstance(availability, DisponibilidadTienda):
            id_value = availability.id_tie
        else:
            id_value = availability.id_alm
        elements = [id_value, availability.id_prod, availability.cantidad]
        cur.execute(statement, elements)
        conn.commit()
        cur.close()
        return {"Creado correctamente": {"id": id_value}}
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail="Error en creación de stock")
    finally:
        if conn is not None:
            conn.close()

@router.put("/availability/{id}/", tags=["availability"])
def update_availability(destination: Destino, id: str, availability: DisponibilidadUpdate):
    conn = None
    try:
        if destination is Destino.TIENDA:
            table = "DisponibilidadTienda"
            id_name = "ID_TIE"
        elif destination is Destino.ALMACEN:
            table = "DisponibilidadAlmacen"
            id_name = "ID_ALM"
        conn = get_db_connection()
        cur = conn.cursor()
        statement = f"""
        UPDATE {table}
        SET CANTIDAD = %s
        WHERE {id_name} = %s AND ID_PROD = %s;
        """
        elements = [availability.cantidad, id, availability.id_prod]
        cur.execute(statement, elements)
        conn.commit()
        cur.close()
        return {"Actualizado correctamente": {"id": id}}
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"{destination.value} {id} desconocido/a")
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail="Error en actualización de stock")
    finally:
        if conn is not None:
            conn.close()

@router.delete("/availability/{id}/", tags=["availability"])
def delete_availability(destination: Destino, id: str, id_prod: int):
    conn = None
    try:
        if destination is Destino.TIENDA:
            table = "DisponibilidadTienda"
            id_name = "ID_TIE"
        elif destination is Destino.ALMACEN:
            table = "DisponibilidadAlmacen"
            id_name = "ID_ALM"
        conn = get_db_connection()
        cur = conn.cursor()
        statement = f"""
        DELETE FROM {table}
        WHERE {id_name} = %s AND ID_PROD = {id_prod};
        """
        cur.execute(statement, [id])
        conn.commit()
        cur.close()
        return {"Eliminado correctamente": {"id": id}}
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"{destination.value} {id} desconocido/a")
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail="Error en eliminación de stock")
    finally:
        if conn is not None:
            conn.close()
