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

class CantidadProducto(BaseModel):
    id_prod: int
    cantidad: int

class TransaccionCompra(BaseModel):
    id_trans: int
    dni_emp: str
    dni_cli: str
    id_tie: str
    importe: float
    fecha: datetime
    carrito: List[CantidadProducto]

class TransaccionCompraInsert(BaseModel):
    dni_emp: str
    dni_cli: str
    id_tie: str
    carrito: List[CantidadProducto]

@router.get("/purchases/", tags=["purchases"])
def get_purchases() -> List[TransaccionCompra]:
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        SELECT *
        FROM Transaccion
        LIMIT 20
        """
        cur.execute(statement)
        result = cur.fetchall()
        purchases = [dict((cur.description[i][0], value)
                         for i, value in enumerate(row)) for row in result]
        for purchase in purchases:
            id_comp = purchase.pop("id_comp")
            purchase["carrito"] = []
            aux_statement = """
            SELECT id_prod, cantidad
            FROM CARRITO
            WHERE ID_COMP = %s
            """
            cur.execute(aux_statement, [id_comp])
            aux_result = cur.fetchall()
            for row in aux_result:
                purchase["carrito"].append(dict((cur.description[i][0], value)
                                                for i, value in enumerate(row)))
        cur.close()
        return purchases
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail="Error en lectura de compras")
    finally:
        if conn is not None:
            conn.close()

# por tienda
@router.get("/purchases/store/{id_tie}/", tags=["purchases"])
def get_purchases_by_store(id_tie: str) -> List[TransaccionCompra]:
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        SELECT *
        FROM Transaccion
        WHERE ID_TIE = %s
        LIMIT 20
        """
        cur.execute(statement, [id_tie])
        result = cur.fetchall()
        purchases = [dict((cur.description[i][0], value)
                         for i, value in enumerate(row)) for row in result]
        for purchase in purchases:
            id_comp = purchase.pop("id_comp")
            purchase["carrito"] = []
            aux_statement = """
            SELECT id_prod, cantidad
            FROM CARRITO
            WHERE ID_COMP = %s
            """
            cur.execute(aux_statement, [id_comp])
            aux_result = cur.fetchall()
            for row in aux_result:
                purchase["carrito"].append(dict((cur.description[i][0], value)
                                                for i, value in enumerate(row)))
        cur.close()
        return purchases
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail="Error en lectura de compras")
    finally:
        if conn is not None:
            conn.close()

# por cliente
@router.get("/purchases/client/{dni_cli}/", tags=["purchases"])
def get_purchases_by_client(dni_cli: str) -> List[TransaccionCompra]:
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        SELECT *
        FROM Transaccion
        WHERE DNI_CLI = %s
        LIMIT 20
        """
        cur.execute(statement, [dni_cli])
        result = cur.fetchall()
        purchases = [dict((cur.description[i][0], value)
                         for i, value in enumerate(row)) for row in result]
        for purchase in purchases:
            id_comp = purchase.pop("id_comp")
            purchase["carrito"] = []
            aux_statement = """
            SELECT id_prod, cantidad
            FROM CARRITO
            WHERE ID_COMP = %s
            """
            cur.execute(aux_statement, [id_comp])
            aux_result = cur.fetchall()
            for row in aux_result:
                purchase["carrito"].append(dict((cur.description[i][0], value)
                                                for i, value in enumerate(row)))
        cur.close()
        return purchases
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail="Error en lectura de compras")
    finally:
        if conn is not None:
            conn.close()

@router.post("/purchases/", status_code=201, tags=["purchases"])
def insert_purchase(purchase: TransaccionCompraInsert):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        INSERT INTO Compra
        VALUES (DEFAULT)
        RETURNING id_comp
        """
        cur.execute(statement)
        id_comp = cur.fetchone()[0]

        if len(purchase.carrito) == 0:
            raise ValueError()

        for item in purchase.carrito:
            aux_statement = """
            INSERT INTO Carrito (id_comp, id_prod, cantidad)
            VALUES (%s, %s, %s)
            """
            cur.execute(aux_statement, [id_comp, item.id_prod, item.cantidad])

        statement = """
        INSERT INTO Transaccion (dni_emp, dni_cli, id_tie, id_comp)
        VALUES (%s, %s, %s, %s)
        """
        cur.execute(statement, [purchase.dni_emp, purchase.dni_cli, purchase.id_tie, id_comp])
        conn.commit()
        cur.close()
        return {"Insertado correctamente": {"id_comp": id_comp}}
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail="Error en inserción de compra")
    except ValueError:
        raise HTTPException(
            status_code=400, detail=f"Carrito vacío")
    finally:
        if conn is not None:
            conn.close()
