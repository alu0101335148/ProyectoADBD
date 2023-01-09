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

class Producto(BaseModel):
    id_prod: int
    nombre: str
    distribuidor: str
    marca: str
    precio: float
    descripcion: str
    categoria: str
    fechacaducidad: Union[date, None] = None

class ProductoInsert(BaseModel):
    nombre: str
    distribuidor: str
    marca: str
    precio: float
    descripcion: str
    categoria: str
    fechacaducidad: Union[date, None] = None

class ProductoUpdate(BaseModel):
    nombre: Union[str, None] = None
    distribuidor: Union[str, None] = None
    marca: Union[str, None] = None
    precio: Union[float, None] = None
    descripcion: Union[str, None] = None
    categoria: Union[str, None] = None
    fechacaducidad: Union[date, None] = None

@router.get("/products/", tags=["products"])
def get_products() -> List[Producto]:
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        SELECT ID_PROD, Nombre, Distribuidor, Marca, Precio, Descripcion, Categoria, FechaCaducidad
        FROM producto
        LIMIT 20;
        """
        cur.execute(statement)
        result = cur.fetchall()

        cur.close()
        # return a json with the result of the query
        products = [dict((cur.description[i][0], value)
                         for i, value in enumerate(row)) for row in result]
        return products
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail=f"Error en lectura de productos: {e.pgerror}")
    finally:
        if conn is not None:
            conn.close()

@router.get("/products/{product_id}/", tags=["products"])
def get_product(product_id: int) -> Producto:
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        SELECT ID_PROD, Nombre, Distribuidor, Marca, Precio, Descripcion, Categoria, FechaCaducidad
        FROM producto 
        WHERE ID_PROD = %s;
        """
        cur.execute(statement, [product_id])
        result = cur.fetchall()

        # Check whether it is a valid product id or not.
        if not result:
            raise ValueError()
        product = result[0]

        cur.close()
        # return a json with the result of the query
        # product = [dict((cur.description[i][0], value) for i, value in enumerate(product))]
        return {cur.description[i][0]: value for i, value in enumerate(product)}
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Producto {product_id} desconocido")
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail=f"Error en lectura de productos: {e.pgerror}")
    finally:
        if conn is not None:
            conn.close()

@router.post("/products/", tags=["products"])
def insert_products(new_product: ProductoInsert):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        INSERT INTO Producto
        VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s);
        """
        elements = [
            new_product.nombre, 
            new_product.distribuidor, 
            new_product.marca, 
            new_product.precio, 
            new_product.descripcion, 
            new_product.categoria, 
            new_product.fecha_caducidad,
        ]
        cur.execute(statement, elements)
        conn.commit()
        cur.close()
        return {"Insertado correctamente": {"nombre": new_product.nombre}}
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error en la inserción de productos: {e.pgerror}"
        )
    finally:
        if conn is not None:
            conn.close()

@router.put("/products/{product_id}/", tags=["products"])
def update_products(product_id: int, updated_product: ProductoUpdate):
    # update only the fields that are not None
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # get the prevoius values of the product and update only the fields that are not None
        statement = """
        SELECT Nombre, Distribuidor, Marca, Precio, Descripcion, Categoria, FechaCaducidad
        FROM producto
        WHERE ID_PROD = %s;
        """
        cur.execute(statement, [product_id])
        result = cur.fetchall()
        
        # Check whether it is a valid product id or not.
        if not result:
            raise ValueError()
        
        # get the previous values
        product = list(result[0])

        # update only the fields that are not None
        if updated_product.nombre is not None:
            product[0] = updated_product.nombre
        if updated_product.distribuidor is not None:
            product[1] = updated_product.distribuidor
        if updated_product.marca is not None:
            product[2] = updated_product.marca
        if updated_product.precio is not None:
            product[3] = updated_product.precio
        if updated_product.descripcion is not None:
            product[4] = updated_product.descripcion
        if updated_product.categoria is not None:
            product[5] = updated_product.categoria
        if updated_product.fecha_caducidad is not None:
            product[6] = updated_product.fecha_caducidad
        
        # update the product
        statement = """
        UPDATE Producto
        SET Nombre = %s, Distribuidor = %s, Marca = %s, Precio = %s, Descripcion = %s, Categoria = %s, FechaCaducidad = %s
        WHERE ID_PROD = %s;
        """
        cur.execute(statement, product + [product_id])
        conn.commit()
        cur.close()
        return {"Actualizado correctamente": {"id": product_id}}
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Producto {product_id} desconocido")
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error en la actualización de productos: {e.pgerror}"
        )
    finally:
        if conn is not None:
            conn.close()

@router.delete("/products/{product_id}/", tags=["products"])
def delete_products(product_id: int):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        statement = """
        DELETE FROM Producto
        WHERE ID_PROD = %s;
        """
        cur.execute(statement, [product_id])
        conn.commit()
        cur.close()
        return {"Borrado correctamente": {"id": product_id}}
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error en la eliminación de productos: {e.pgerror}"
        )
    finally:
        if conn is not None:
            conn.close()
