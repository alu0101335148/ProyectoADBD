-- Script de creación de la base de datos.

-- CREATE DATABASE SUPERMERCADO;

CREATE TYPE PUESTO as ENUM ('Cajero', 'Charcuteria', 'Logistica', 'Gerente', 'Pescaderia', 'Carniceria');

CREATE TYPE CATEGORIAS AS ENUM ('Alimentacion', 'Limpieza', 'Higiene', 'Textil', 'Herramientas', 'Otros');

CREATE TABLE Cliente(
    DNI_CLI VARCHAR(9) PRIMARY KEY,
    Nombre VARCHAR(30) NOT NULL,
    Apellidos VARCHAR(30) NOT NULL,
    Correo VARCHAR(30),
    Telefono VARCHAR(9),
    Calle VARCHAR(30) NOT NULL,
    Ciudad VARCHAR(30) NOT NULL,
    Provincia VARCHAR(30) NOT NULL,
    Descuento FLOAT DEFAULT 0
);

CREATE TABLE Producto(
    ID_PROD SERIAL PRIMARY KEY,
    Nombre VARCHAR(30) NOT NULL,
    Distribuidor VARCHAR(30) NOT NULL,
    Marca VARCHAR(30) NOT NULL,
    Precio FLOAT NOT NULL,
    Descripcion VARCHAR(150) NOT NULL,
    Categoria CATEGORIAS NOT NULL,
    FechaCaducidad DATE
);

CREATE TABLE Empleado(
    DNI_EMP VARCHAR(9) PRIMARY KEY,
    Nombre VARCHAR(30) NOT NULL,
    Apellidos VARCHAR(30) NOT NULL,
    Calle VARCHAR(30) NOT NULL,
    Ciudad VARCHAR(30) NOT NULL,
    Provincia VARCHAR(30) NOT NULL,
    Salario FLOAT NOT NULL,
    HoraEntrada TIME NOT NULL,
    HoraSalida TIME NOT NULL,
    NumCuenta VARCHAR(30) NOT NULL,
    Rol PUESTO NOT NULL
);

CREATE TABLE Cajero(
    DNI_EMP VARCHAR(9) PRIMARY KEY,
    Caja INT NOT NULL,
    FOREIGN KEY (DNI_EMP) REFERENCES Empleado(DNI_EMP) ON DELETE CASCADE
);

CREATE TABLE Charcuteria(
    DNI_EMP VARCHAR(9) PRIMARY KEY,
    Cortadora INT NOT NULL,
    FOREIGN KEY (DNI_EMP) REFERENCES Empleado(DNI_EMP) ON DELETE CASCADE
);

CREATE TABLE Logistica(
    DNI_EMP VARCHAR(9) PRIMARY KEY,
    Montacargas INT NOT NULL,
    FOREIGN KEY (DNI_EMP) REFERENCES Empleado(DNI_EMP) ON DELETE CASCADE
);

CREATE TABLE Tienda(
    ID_TIE VARCHAR(30) PRIMARY KEY,
    Calle VARCHAR(30) NOT NULL,
    Ciudad VARCHAR(30) NOT NULL,
    Provincia VARCHAR(30) NOT NULL,
    Superficie FLOAT NOT NULL
);

CREATE TABLE Almacen(
    ID_ALM VARCHAR(30) PRIMARY KEY,
    Temperatura FLOAT NOT NULL,
    Superficie FLOAT NOT NULL,
    DNI_SUPER VARCHAR(9),
    FOREIGN KEY (ID_ALM) REFERENCES Tienda(ID_TIE) ON DELETE CASCADE,
    FOREIGN KEY (DNI_SUPER) REFERENCES Empleado(DNI_EMP) ON DELETE SET NULL
);

CREATE TABLE Trabaja(
    DNI_EMP VARCHAR(9),
    ID_TIE VARCHAR(30),
    FechaInicio DATE,
    FechaFin DATE,
    FOREIGN KEY (DNI_EMP) REFERENCES Empleado(DNI_EMP) ON DELETE CASCADE,
    FOREIGN KEY (ID_TIE) REFERENCES Tienda(ID_TIE) ON DELETE CASCADE,
    PRIMARY KEY (DNI_EMP, ID_TIE, FechaInicio)
);

CREATE TABLE DisponibilidadTienda(
    ID_TIE VARCHAR(30),
    ID_PROD INT,
    Cantidad INT NOT NULL,
    FOREIGN KEY (ID_TIE) REFERENCES Tienda(ID_TIE) ON DELETE CASCADE,
    FOREIGN KEY (ID_PROD) REFERENCES Producto(ID_PROD) ON DELETE CASCADE,
    PRIMARY KEY (ID_TIE, ID_PROD)
);

CREATE TABLE DisponibilidadAlmacen(
    ID_ALM VARCHAR(30),
    ID_PROD INT,
    Cantidad INT NOT NULL,
    FOREIGN KEY (ID_ALM) REFERENCES Almacen(ID_ALM) ON DELETE CASCADE,
    FOREIGN KEY (ID_PROD) REFERENCES Producto(ID_PROD) ON DELETE CASCADE,
    PRIMARY KEY (ID_ALM, ID_PROD)
);

CREATE TABLE Compra(
    ID_COMP SERIAL PRIMARY KEY
);

CREATE TABLE Transaccion(
    ID_TRANS SERIAL PRIMARY KEY,
    DNI_CLI VARCHAR(9),
    DNI_EMP VARCHAR(9),
    ID_TIE VARCHAR(30),
    ID_COMP INT UNIQUE,
    Importe FLOAT,
    Fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (DNI_CLI) REFERENCES Cliente(DNI_CLI) ON DELETE SET NULL,
    FOREIGN KEY (DNI_EMP) REFERENCES Empleado(DNI_EMP) ON DELETE SET NULL,
    FOREIGN KEY (ID_TIE) REFERENCES Tienda(ID_TIE) ON DELETE SET NULL,
    FOREIGN KEY (ID_COMP) REFERENCES Compra(ID_COMP) ON DELETE CASCADE
);

CREATE TABLE Carrito(
    ID_COMP INT,
    ID_PROD INT,
    Cantidad INT NOT NULL,
    FOREIGN KEY (ID_PROD) REFERENCES Producto(ID_PROD) ON DELETE CASCADE,
    FOREIGN KEY (ID_COMP) REFERENCES Compra(ID_COMP) ON DELETE CASCADE,
    PRIMARY KEY (ID_COMP, ID_PROD)
);

ALTER TABLE Producto
ADD CONSTRAINT PrecioPositivo CHECK (Precio >= 0);

ALTER TABLE Transaccion
ADD CONSTRAINT ImportePositivo CHECK (Importe >= 0);

ALTER TABLE Carrito
ADD CONSTRAINT CantidadPositiva CHECK (Cantidad > 0);

ALTER TABLE Cliente
ADD CONSTRAINT DescuentoPositivo CHECK (Descuento >= 0 AND Descuento <= 25);


-- El número de caja, cortadora y montacargas no puede ser negativo.

ALTER TABLE Cajero
ADD CONSTRAINT CajaPositiva CHECK (Caja >= 0);

ALTER TABLE Charcuteria
ADD CONSTRAINT CortadoraPositiva CHECK (Cortadora >= 0);

ALTER TABLE Logistica
ADD CONSTRAINT MontacargasPositivo CHECK (Montacargas >= 0);

-- La fecha de inicio de trabajo no puede ser posterior a la fecha de fin.

ALTER TABLE Trabaja
ADD CONSTRAINT FechaInicioMenorFechaFin CHECK (FechaInicio < FechaFin);

-- La cantidad de productos no puede ser negativa.

ALTER TABLE DisponibilidadTienda
ADD CONSTRAINT CantidadPositiva CHECK (Cantidad >= 0);

ALTER TABLE DisponibilidadAlmacen
ADD CONSTRAINT CantidadPositiva CHECK (Cantidad >= 0);

ALTER TABLE Empleado
ADD CONSTRAINT SalarioPositivo CHECK (Salario >= 900);

ALTER TABLE Tienda
ADD CONSTRAINT SuperficiePositiva CHECK (Superficie > 0);

ALTER TABLE Almacen
ADD CONSTRAINT SuperficiePositiva CHECK (Superficie > 0);

--Inserción de disparadores

CREATE OR REPLACE FUNCTION check_supervisa()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT COUNT(*) 
        FROM Trabaja JOIN Logistica USING (DNI_EMP)
        WHERE DNI_EMP = NEW.DNI_SUPER AND 
        ID_TIE = NEW.ID_ALM) = 0 THEN
      RAISE EXCEPTION 'El empleado % no ha trabajado nunca en la tienda %', NEW.DNI_SUPER, NEW.ID_ALM;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_supervisa_trigger
BEFORE INSERT OR UPDATE ON Almacen
FOR EACH ROW
EXECUTE PROCEDURE check_supervisa();

-- Aplica un descuento de 10 a los clientes que el último mes hayan gastado más de 100 euros.
CREATE OR REPLACE FUNCTION check_descuento()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT SUM(Importe) 
        FROM Transaccion
        WHERE DNI_CLI = NEW.DNI_CLI AND
        Fecha > (SELECT CURRENT_TIMESTAMP - INTERVAL '1 month')) > 100 THEN
      UPDATE Cliente
      SET Descuento = 10
      WHERE DNI_CLI = NEW.DNI_CLI;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_descuento_trigger
AFTER UPDATE ON Transaccion
FOR EACH ROW
EXECUTE PROCEDURE check_descuento();

-- Calcula el importe en base a la lista de productos que se han comprado. 
-- Nota: en caso de que tenga descuento lo aplica y lo pone a 0.
CREATE OR REPLACE FUNCTION check_importe()
RETURNS TRIGGER AS $$
BEGIN
    -- Calcula el importe de la compra
    SELECT SUM(p.Precio * c.Cantidad) INTO NEW.importe
    FROM Carrito c
    INNER JOIN Producto p ON c.ID_PROD = p.ID_PROD
    WHERE c.ID_COMP = NEW.ID_COMP;

    -- En caso de que la compra sea superior a 50€ y tenga descuento lo aplica
    IF NEW.Importe > 50 AND NEW.DNI_CLI IN (SELECT DNI_CLI FROM Cliente WHERE Descuento > 0) THEN
        NEW.Importe = NEW.importe - (SELECT Descuento FROM Cliente WHERE DNI_CLI = NEW.DNI_CLI);
        -- Pone a 0 el descuento
        UPDATE Cliente
        SET Descuento = 0
        WHERE DNI_CLI = NEW.DNI_CLI;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_importe_trigger
BEFORE INSERT ON Transaccion
FOR EACH ROW
EXECUTE PROCEDURE check_importe();

-- Revisar que en una transacción no se pueda comprar un producto del carrito que no esté en la tienda
-- de igual forma que haya stock suficiente.
CREATE OR REPLACE FUNCTION check_producto()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT * FROM Carrito c JOIN Producto p USING (ID_PROD) 
            WHERE c.ID_COMP = NEW.ID_COMP AND EXISTS (
                SELECT * FROM DisponibilidadTienda 
                WHERE ID_PROD = p.ID_PROD AND ID_TIE = NEW.ID_TIE AND Cantidad < c.Cantidad
            )
    ) THEN
      RAISE EXCEPTION 'No hay stock suficiente de alguno de los productos de la compra %', NEW.ID_COMP;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_producto_trigger
BEFORE INSERT OR UPDATE ON Transaccion
FOR EACH ROW
EXECUTE PROCEDURE check_producto();

-- Revisar que en una transacción no te pueda atender un empleado que no sea cajero en esa tienda
CREATE OR REPLACE FUNCTION check_cajero()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT COUNT(*) 
        FROM Trabaja JOIN Cajero USING (DNI_EMP) 
        WHERE DNI_EMP = NEW.DNI_EMP AND 
        ID_TIE = NEW.ID_TIE) = 0 THEN
      RAISE EXCEPTION 'El empleado % no es cajero en la tienda %', NEW.DNI_EMP, NEW.ID_TIE;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_cajero_trigger
BEFORE INSERT OR UPDATE ON Transaccion
FOR EACH ROW
EXECUTE PROCEDURE check_cajero();

-- Eliminar el stock una vez se ha hecho la transaccion
CREATE OR REPLACE FUNCTION update_stock()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE DisponibilidadTienda
    SET Cantidad = Cantidad - c.Cantidad
    FROM Carrito c
    WHERE c.ID_COMP = NEW.ID_COMP AND 
          DisponibilidadTienda.ID_PROD = c.ID_PROD AND 
          DisponibilidadTienda.ID_TIE = NEW.ID_TIE;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_stock_trigger
AFTER INSERT ON Transaccion
FOR EACH ROW
EXECUTE PROCEDURE update_stock();
