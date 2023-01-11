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

class Cliente(BaseModel):
    dni_cli: str
    nombre: str
    apellidos: str
    correo: str
    telefono: str
    calle: str
    ciudad: str
    provincia: str

class ClienteUpdate(BaseModel):
    nombre: Union[str, None] = None
    apellidos: Union[str, None] = None
    correo: Union[str, None] = None
    telefono: Union[str, None] = None
    calle: Union[str, None] = None
    ciudad: Union[str, None] = None
    provincia: Union[str, None] = None
    descuento: Union[float, None] = None

@router.get("/clients/", tags=["clients"])
def get_clients() -> List[Cliente]:
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        SELECT *
        FROM Cliente
        LIMIT 20;
        """
        cur.execute(statement)
        result = cur.fetchall()

        cur.close()
        # return a json with the result of the query
        clients = [dict((cur.description[i][0], value)
                         for i, value in enumerate(row)) for row in result]
        return clients
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail="Error en lectura de clientes")
    finally:
        if conn is not None:
            conn.close()    

@router.get("/clients/{client_DNI}/", tags=["clients"])
def get_client(client_DNI: str) -> Cliente:
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        SELECT *
        FROM Cliente 
        WHERE DNI_CLI = %s;
        """
        cur.execute(statement, [client_DNI])
        result = cur.fetchall()

        # Check whether it is a valid client id or not.
        if not result:
            raise ValueError()
        client = result[0]

        cur.close()
        # return a json with the result of the query
        return {cur.description[i][0]: value for i, value in enumerate(client)}
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Cliente {client_DNI} desconocido")
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail="Error en lectura de clientes")
    finally:
        if conn is not None:
            conn.close()

@router.post("/clients/", status_code=201, tags=["clients"])
def insert_clients(new_client: Cliente):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        INSERT INTO Cliente 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        elements = [
            new_client.id_cli,
            new_client.nombre,
            new_client.apellidos,
            new_client.correo,
            new_client.telefono,
            new_client.calle,
            new_client.ciudad,
            new_client.provincia,
        ]
        cur.execute(statement, elements)
        conn.commit()
        cur.close()
        return {"Insertado correctamente": {"nombre": new_client.nombre}}
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, 
            detail="Error en la inserción de clientes"
        )
    finally:
        if conn is not None:
            conn.close()

@router.put("/clients/{client_DNI}/", tags=["clients"])
def update_clients(client_DNI: str, updated_client: ClienteUpdate):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        SELECT Nombre, Apellidos, Correo, Telefono, Calle, Ciudad, Provincia, Descuento
        FROM Cliente 
        WHERE DNI_CLI = %s;
        """
        cur.execute(statement, [client_DNI])
        result = cur.fetchall()

        # Check whether it is a valid client id or not.
        if not result:
            raise ValueError()
        
        # get the previous values
        client = list(result[0])

        # update only the fields that are not None
        if updated_client.nombre is not None:
            client[0] = updated_client.nombre
        if updated_client.apellidos is not None:
            client[1] = updated_client.apellidos
        if updated_client.correo is not None:
            client[2] = updated_client.correo
        if updated_client.telefono is not None:
            client[3] = updated_client.telefono
        if updated_client.calle is not None:
            client[4] = updated_client.calle
        if updated_client.ciudad is not None:
            client[5] = updated_client.ciudad
        if updated_client.provincia is not None:
            client[6] = updated_client.provincia
        if updated_client.descuento is not None:
            client[7] = updated_client.descuento
        
        # update the product
        statement = """
        UPDATE Cliente
        SET Nombre = %s, Apellidos = %s, Correo = %s, Telefono = %s, Calle = %s, Ciudad = %s, Provincia = %s, Descuento = %s
        WHERE DNI_CLI = %s;
        """
        cur.execute(statement, client + [client_DNI])
        conn.commit()
        cur.close()
        return {"Actualizado correctamente": {"id": client_DNI}}
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Cliente {client_DNI} desconocido")
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, 
            detail="Error en la actualización de clientes"
        )
    finally:
        if conn is not None:
            conn.close()

@router.delete("/clients/{client_DNI}/", tags=["clients"])
def delete_clients(client_DNI: str):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        DELETE FROM Cliente 
        WHERE DNI_CLI = %s;
        """
        cur.execute(statement, [client_DNI])
        conn.commit()
        cur.close()
        return {"Eliminado correctamente": {"id": client_DNI}}
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, 
            detail="Error en la eliminación de clientes"
        )
    finally:
        if conn is not None:
            conn.close()
