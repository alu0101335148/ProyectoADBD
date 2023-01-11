from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from enum import Enum
from typing import Union, List
from datetime import date, time, datetime
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )
    return conn

class Tienda(BaseModel):
    id_tie: str
    calle: str
    ciudad: str
    provincia: str
    superficie: float

class TiendaUpdate(BaseModel):
    calle: Union[str, None] = None
    ciudad: Union[str, None] = None
    provincia: Union[str, None] = None
    superficie: Union[float, None] = None

@router.get("/stores/", tags=["stores"])
def get_stores() -> List[Tienda]:
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        SELECT *
        FROM Tienda
        LIMIT 20;
        """
        cur.execute(statement)
        result = cur.fetchall()

        cur.close()
        # return a json with the result of the query
        stores = [dict((cur.description[i][0], value)
                         for i, value in enumerate(row)) for row in result]
        return stores
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail="Error en lectura de tiendas")
    finally:
        if conn is not None:
            conn.close()    

@router.get("/stores/{store_id}/", tags=["stores"])
def get_store(store_id: str) -> Tienda:
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        SELECT *
        FROM Tienda 
        WHERE ID_TIE = %s;
        """
        cur.execute(statement, [store_id])
        result = cur.fetchall()

        # Check whether it is a valid store id or not.
        if not result:
            raise ValueError()
        store = result[0]

        cur.close()
        # return a json with the result of the query
        return {cur.description[i][0]: value for i, value in enumerate(store)}
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Tienda {store_id} desconocida")
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail="Error en lectura de tiendas")
    finally:
        if conn is not None:
            conn.close()

@router.post("/stores/", status_code=201, tags=["stores"])
def create_stores(new_store: Tienda):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        INSERT INTO Tienda 
        VALUES (%s, %s, %s, %s, %s);
        """
        elements = [
            new_store.id_tie,
            new_store.calle,
            new_store.ciudad,
            new_store.provincia,
            new_store.superficie
        ]
        cur.execute(statement, elements)
        conn.commit()
        cur.close()
        return {"Insertada correctamente": {"id": new_store.id_tie}}
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, 
            detail="Error en la inserción de tiendas"
        )
    finally:
        if conn is not None:
            conn.close()

@router.put("/stores/{store_id}/", tags=["stores"])
def update_stores(store_id: str, updated_store: TiendaUpdate):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        SELECT Calle, Ciudad, Provincia, Superficie
        FROM Tienda 
        WHERE ID_TIE = %s;
        """
        cur.execute(statement, [store_id])
        result = cur.fetchall()

        # Check whether it is a valid store id or not.
        if not result:
            raise ValueError()
        
        # get the previous values
        store = list(result[0])

        # update only the fields that are not None
        if updated_store.calle is not None:
            store[0] = updated_store.calle
        if updated_store.ciudad is not None:
            store[1] = updated_store.ciudad
        if updated_store.provincia is not None:
            store[2] = updated_store.provincia
        if updated_store.superficie is not None:
            store[3] = updated_store.superficie

        # update the product
        statement = """
        UPDATE Tienda
        SET Calle = %s, Ciudad = %s, Provincia = %s, Superficie = %s
        WHERE ID_TIE = %s;
        """
        cur.execute(statement, store + [store_id])
        conn.commit()
        cur.close()
        return {"Actualizada correctamente": {"id": store_id}}
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Tienda {store_id} desconocida")
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, 
            detail="Error en la actualización de tiendas"
        )
    finally:
        if conn is not None:
            conn.close()

@router.delete("/stores/{store_id}/", tags=["stores"])
def delete_stores(store_id: str):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        DELETE FROM Tienda 
        WHERE ID_TIE = %s;
        """
        cur.execute(statement, [store_id])
        conn.commit()
        cur.close()
        return {"Eliminada correctamente": {"id": store_id}}
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, 
            detail="Error en la eliminación de tiendas"
        )
    finally:
        if conn is not None:
            conn.close()
