from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from typing import Union, List
from datetime import date
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

API_VERSION = "0.1.1"
TITLE = "Supermercado API"

app = FastAPI(title=TITLE, version=API_VERSION)

@app.get("/")
def root():
    return {"health_check": "OK", "version": API_VERSION}

# *****************************************************************************

class Producto(BaseModel):
    id_prod: int
    nombre: str
    distribuidor: str
    marca: str
    precio: float
    descripcion: str
    categoria: str
    fecha_caducidad: Union[date, None] = None

class ProductoInsert(BaseModel):
    nombre: str
    distribuidor: str
    marca: str
    precio: float
    descripcion: str
    categoria: str
    fecha_caducidad: Union[date, None] = None

class ProductoUpdate(BaseModel):
    nombre: Union[str, None] = None
    distribuidor: Union[str, None] = None
    marca: Union[str, None] = None
    precio: Union[float, None] = None
    descripcion: Union[str, None] = None
    categoria: Union[str, None] = None
    fecha_caducidad: Union[date, None] = None

@app.get("/products/", tags=["products"])
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
            status_code=500, detail="Error en lectura de productos: {e.pgerror}")
    finally:
        if conn is not None:
            conn.close()

@app.get("/products/{product_id}/", tags=["products"])
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
        print(product)

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

@app.post("/products/", tags=["products"])
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

@app.put("/products/{product_id}/", tags=["products"])
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

@app.delete("/products/{product_id}/", tags=["products"])
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

# *****************************************************************************

class Cliente(BaseModel):
    id_cli: str
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

@app.get("/clients/", tags=["clients"])
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
            status_code=500, detail="Error en lectura de clientes: {e.pgerror}")
    finally:
        if conn is not None:
            conn.close()    

@app.get("/clients/{client_DNI}/", tags=["clients"])
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
        print(client)

        cur.close()
        # return a json with the result of the query
        return {cur.description[i][0]: value for i, value in enumerate(client)}
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Cliente {client_DNI} desconocido")
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail=f"Error en lectura de clientes: {e.pgerror}")
    finally:
        if conn is not None:
            conn.close()

@app.post("/clients/", tags=["clients"])
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
            detail=f"Error en la inserción de clientes: {e.pgerror}"
        )
    finally:
        if conn is not None:
            conn.close()

@app.put("/clients/{client_DNI}/", tags=["clients"])
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
            detail=f"Error en la actualización de clientes: {e.pgerror}"
        )
    finally:
        if conn is not None:
            conn.close()

@app.delete("/clients/{client_DNI}/", tags=["clients"])
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
            detail=f"Error en la eliminación de clientes: {e.pgerror}"
        )
    finally:
        if conn is not None:
            conn.close()

# *****************************************************************************

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

@app.get("/stores/", tags=["stores"])
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
            status_code=500, detail="Error en lectura de tiendas: {e.pgerror}")
    finally:
        if conn is not None:
            conn.close()    

@app.get("/stores/{store_id}/", tags=["stores"])
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
        print(store)

        cur.close()
        # return a json with the result of the query
        return {cur.description[i][0]: value for i, value in enumerate(store)}
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Tienda {store_id} desconocida")
    except psycopg2.DatabaseError as e:
        raise HTTPException(
            status_code=500, detail=f"Error en lectura de tiendas: {e.pgerror}")
    finally:
        if conn is not None:
            conn.close()

@app.post("/stores/", tags=["stores"])
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
            detail=f"Error en la inserción de tiendas: {e.pgerror}"
        )
    finally:
        if conn is not None:
            conn.close()

@app.put("/stores/{store_id}/", tags=["stores"])
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
            detail=f"Error en la actualización de tiendas: {e.pgerror}"
        )
    finally:
        if conn is not None:
            conn.close()

@app.delete("/stores/{store_id}/", tags=["stores"])
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
            detail=f"Error en la eliminación de tiendas: {e.pgerror}"
        )
    finally:
        if conn is not None:
            conn.close()

# *****************************************************************************

class Almacen(BaseModel):
    id_alm: str
    temperatura: float
    superficie: float
    dni_super: Union[str, None] = None

class AlmacenUpdate(BaseModel):
    temperatura: Union[float, None] = None
    superficie: Union[float, None] = None
    dni_super: Union[str, None] = None

@app.get("/warehouse/", tags=["warehouse"])
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
            status_code=500, detail="Error en lectura de almacenes: {e.pgerror}")
    finally:
        if conn is not None:
            conn.close()

@app.get("/warehouse/{warehouse_id}/", tags=["warehouse"])
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
        print(warehouse)

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

@app.post("/warehouse/", tags=["warehouse"])
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

@app.put("/warehouse/{warehouse_id}/", tags=["warehouse"])
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

@app.delete("/warehouse/{warehouse_id}/", tags=["warehouse"])
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

# *****************************************************************************

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

@app.get("/availability/", tags=["availability"])
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
            status_code=500, detail=f"Error en lectura de stock: {e.pgerror}")
    finally:
        if conn is not None:
            conn.close()

@app.get("/availability/{id}/", tags=["availability"])
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
            status_code=500, detail=f"Error en lectura de stock: {e.pgerror}")
    finally:
        if conn is not None:
            conn.close()

@app.post("/availability/", tags=["availability"])
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
            status_code=500, detail=f"Error en creación de stock: {e.pgerror}")
    finally:
        if conn is not None:
            conn.close()

@app.put("/availability/{id}/", tags=["availability"])
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
            status_code=500, detail=f"Error en actualización de stock: {e.pgerror}")
    finally:
        if conn is not None:
            conn.close()

@app.delete("/availability/{id}/", tags=["availability"])
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
            status_code=500, detail=f"Error en eliminación de stock: {e.pgerror}")
    finally:
        if conn is not None:
            conn.close()