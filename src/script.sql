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
    ID_COMP INT NOT NULL,
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
        FROM Trabaja 
        WHERE DNI_EMP = NEW.DNI_SUPER AND 
        ID_TIE = NEW.ID_ALM) = 0 THEN
      RAISE EXCEPTION 'El empleado % no trabaja en la tienda %', NEW.DNI_SUPER, NEW.ID_ALM;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_supervisa_trigger
BEFORE INSERT OR UPDATE ON Almacen
FOR EACH ROW
EXECUTE PROCEDURE check_supervisa();

CREATE OR REPLACE FUNCTION check_descuento()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT SUM(Importe)
        FROM Transaccion
        WHERE DNI_CLI = NEW.DNI_CLI) >= 100 THEN
      UPDATE Cliente SET Descuento = 10 WHERE DNI_CLI = NEW.DNI_CLI;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_descuento_trigger
AFTER INSERT OR UPDATE ON Transaccion
FOR EACH ROW
EXECUTE PROCEDURE check_descuento();

CREATE OR REPLACE FUNCTION check_importe()
RETURNS TRIGGER AS $$
BEGIN
    NEW.Importe = (SELECT SUM(Cantidad * Precio)
                   FROM Transaccion JOIN Compra USING (ID_COMP)
                   JOIN Carrito USING (ID_COMP)
                   JOIN Producto USING (ID_PROD)
                   WHERE ID_TRANS = NEW.ID_TRANS
                );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_importe_trigger
BEFORE INSERT OR UPDATE ON Transaccion
FOR EACH ROW
EXECUTE PROCEDURE check_importe();
