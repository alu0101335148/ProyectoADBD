# ProyectoADBD

## Modelo relacional

Cliente (**DNI_CLI**, Nombre, Apellidos, Correo, Telefono, Calle, Ciudad, Provincia, ~~Descuento~~)

Producto (**ID_PROD**, Nombre, Distribuidor, Marca, Precio, Descripción, Categoría, FechaCaducidad)

Empleado(**DNI_EMP**, Nombre, Apellidos, Calle, Ciudad, Provincia, Salario, HoraEntrada, HoraSalida, NumCuenta, rol)

Cajero(***DNI_EMP***, Caja)<br>
Foreing Key (DNI_EMP) references Empleado(DNI_EMP)

Charcutería(***DNI_EMP***, Cortadora)<br>
Foreing Key (DNI_EMP) references Empleado(DNI_EMP)

Logistica(***DNI_EMP***, Montagarcas)<br>
Foreing Key (DNI_EMP) references Empleado(DNI_EMP)

Tienda(**ID_TIE**, Calle, Ciudad, Provincia, Superficie)

Almacen(***ID_ALM***, Temperatura, Superficie, *ID_EMP*)<br>
Foreing Key (ID_ALM) references Tienda(ID_TIE)
Foreing Key (ID_EMP) references Empleado(DNI_EMP)

Trabaja(***DNI_EMP***, ***ID_TIE***, **FechaInicio**, FechaFin)<br>
Foreing Key (DNI_EMP) references Empleado(DNI_EMP)<br>
Foreing Key (ID_TIE) references Tienda(ID_TIE)

DisponibilidadTienda(***ID_TIE***, ***ID_PROD***, Cantidad)<br>
Foreing Key (ID_TIE) references Tienda(ID_TIE)<br>
Foreing Key (ID_PROD) references Producto(ID_PROD)

DisponibilidadAlmacen(***ID_ALM***, ***ID_PROD***, Cantidad)<br>
Foreing Key (ID_ALM) references Almacen(ID_ALM)<br>
Foreing Key (ID_PROD) references Producto(ID_PROD)

Compra(***ID_PED***, ***ID_PROD***, Cantidad)
Foreing Key (ID_PED) references Transaccion(ID_TRANS)
Foreing Key (ID_PROD) references Producto(ID_PROD)

Transaccion(**ID_TRANS**, Fecha, **DNI_CLI**, **DNI_EMP**, **ID_TIE**, ~~Importe~~)

## Creación de la base de datos y los tipos de datos

```sql
CREATE DATABASE SUPERMERCADO;

CREATE TYPE PUESTO as ENUM ('Cajero', 'Charcuteria', 'Logistica', 'Gerente', 'Pescaderia', 'Carniceria');

CREATE TYPE CATEGORIAS AS ENUM ('Alimentacion', 'Limpieza', 'Higiene', 'Textil', 'Herramientas', 'Otros');
```

## Creación de tablas

```sql
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
    ID_EMP VARCHAR(9),
    FOREIGN KEY (ID_ALM) REFERENCES Tienda(ID_TIE) ON DELETE CASCADE,
    FOREIGN KEY (ID_EMP) REFERENCES Empleado(DNI_EMP) ON SET NULL
);

CREATE TABLE Trabaja(
    DNI_EMP VARCHAR(9) PRIMARY KEY,
    ID_TIE VARCHAR(30) PRIMARY KEY,
    FechaInicio DATE PRIMARY KEY,
    FechaFin DATE,
    FOREIGN KEY (DNI_EMP) REFERENCES Empleado(DNI_EMP) ON DELETE CASCADE,
    FOREIGN KEY (ID_TIE) REFERENCES Tienda(ID_TIE) ON DELETE CASCADE
);

CREATE TABLE DisponibilidadTienda(
    ID_TIE VARCHAR(30) PRIMARY KEY,
    ID_PROD INT PRIMARY KEY,
    Cantidad INT NOT NULL,
    FOREIGN KEY (ID_TIE) REFERENCES Tienda(ID_TIE) ON DELETE CASCADE,
    FOREIGN KEY (ID_PROD) REFERENCES Producto(ID_PROD) ON DELETE CASCADE
);

CREATE TABLE DisponibilidadAlmacen(
    ID_ALM VARCHAR(30) PRIMARY KEY,
    ID_PROD INT PRIMARY KEY,
    Cantidad INT NOT NULL,
    FOREIGN KEY (ID_ALM) REFERENCES Almacen(ID_ALM) ON DELETE CASCADE,
    FOREIGN KEY (ID_PROD) REFERENCES Producto(ID_PROD) ON DELETE CASCADE
);

CREATE TABLE Transaccion(
    ID_TRANS SERIAL PRIMARY KEY,
    Fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    DNI_CLI VARCHAR(9),
    DNI_EMP VARCHAR(9),
    ID_TIE VARCHAR(30),
    Importe FLOAT NOT NULL,
    FOREIGN KEY (DNI_CLI) REFERENCES Cliente(DNI_CLI) ON DELETE SET NULL,
    FOREIGN KEY (DNI_EMP) REFERENCES Empleado(DNI_EMP) ON DELETE SET NULL,
    FOREIGN KEY (ID_TIE) REFERENCES Tienda(ID_TIE) ON DELETE SET NULL
);

CREATE TABLE Compra(
    ID_PED INT PRIMARY KEY,
    ID_PROD INT PRIMARY KEY,
    Cantidad INT NOT NULL,
    FOREIGN KEY (ID_PED) REFERENCES Transaccion(ID_TRANS) ON DELETE CASCADE,
    FOREIGN KEY (ID_PROD) REFERENCES Producto(ID_PROD) ON DELETE CASCADE
);
```

## Inserción de restricciones

El precio de los productos y de los importes de las transacciones no pueden ser negativos.

```sql
ALTER TABLE Producto
ADD CONSTRAINT PrecioPositivo CHECK (Precio >= 0);

ALTER TABLE Transaccion
ADD CONSTRAINT ImportePositivo CHECK (Importe >= 0);
```

El descuento de los clientes no puede ser negativo ni mayor que 25.

```sql
ALTER TABLE Cliente
ADD CONSTRAINT DescuentoPositivo CHECK (Descuento >= 0 AND Descuento <= 25);
```

La hora de entrada no puede ser posterior a la hora de salida.

```sql
ALTER TABLE Empleado
ADD CONSTRAINT HoraEntradaMenorHoraSalida CHECK (HoraEntrada < HoraSalida);
```

El número de caja, cortadora y montacargas no puede ser negativo.

```sql
ALTER TABLE Caja
ADD CONSTRAINT CajaPositiva CHECK (Caja >= 0);

ALTER TABLE Charcuteria
ADD CONSTRAINT CortadoraPositiva CHECK (Cortadora >= 0);

ALTER TABLE Logistica
ADD CONSTRAINT MontacargasPositivo CHECK (Montacargas >= 0);
```

La fecha de inicio de trabajo no puede ser posterior a la fecha de fin.

```sql
ALTER TABLE Trabaja
ADD CONSTRAINT FechaInicioMenorFechaFin CHECK (FechaInicio < FechaFin);
```

La cantidad de productos no puede ser negativa.

```sql
ALTER TABLE DisponibilidadTienda
ADD CONSTRAINT CantidadPositiva CHECK (Cantidad >= 0);

ALTER TABLE DisponibilidadAlmacen
ADD CONSTRAINT CantidadPositiva CHECK (Cantidad >= 0);
```

El salario no puede inferior a un salario mínimo.

```sql
ALTER TABLE Empleado
ADD CONSTRAINT SalarioPositivo CHECK (Salario >= 900);
```

La superficie debe se positiva.

```sql
ALTER TABLE Tienda
ADD CONSTRAINT SuperficiePositiva CHECK (Superficie > 0);

ALTER TABLE Almacen
ADD CONSTRAINT SuperficiePositiva CHECK (Superficie > 0);
```

## Inserción de disparadores

Trigger para comprobar que empleado no supervisa almacen de tienda en la que no trabaja.

```sql
CREATE OR REPLACE FUNCTION check_supervisa()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT COUNT(*) 
        FROM Trabaja 
        WHERE DNI_EMP = NEW.DNI_EMP AND 
        ID_TIE = NEW.ID_ALM AND 
        FechaFin NOT NULL) = 0 THEN
      RAISE EXCEPTION 'El empleado no trabaja en la tienda';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_supervisa
BEFORE INSERT OR UPDATE ON Almacen
FOR EACH ROW
EXECUTE PROCEDURE check_supervisa();
```

Trigger para asignar un descuento a los clientes que hayan gastado más de 100 €.

```sql
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

CREATE TRIGGER check_descuento
AFTER INSERT OR UPDATE ON Transaccion
FOR EACH ROW
EXECUTE PROCEDURE check_descuento();
```

Trigger para calcular el importe total de una transacción, en base a la cantidad
de producto y precio.

```sql
CREATE OR REPLACE FUNCTION check_importe()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Transaccion
    SET Importe = (SELECT SUM(Cantidad * Precio)
                   FROM Compra JOIN Producto USING (ID_PROD)
                   WHERE ID_PED = NEW.ID_PED)
    WHERE ID_TRANS = NEW.ID_TRANS AND DNI_CLI = NEW.DNI_CLI;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_importe
AFTER INSERT OR UPDATE ON Compra
FOR EACH ROW
EXECUTE PROCEDURE check_importe();
```
