# Proyecto ADBD (Supermercado)

## Integrantes

- Airam Rafael Luque León (alu0101335148@ull.edu.es)

- Andrés Pérez Castellano (alu0101313511@ull.edu.es)

## Objetivos

- Almacenar la información de los productos disponibles en la tienda.

- Almacenar la información del personal designado contratado.

- Contemplar las diferentes categorías de productos de la empresa.

- Contemplar los diferentes roles de los empleados, pudiendo almacenar la 
  información correspondientes de estos, como el cargo, la información 
  personal, horario, etc.

- La base de datos deberá almacenar la información correspondiente a los 
  clientes.

- Almacenar información de interés extraída de las transacciones realizadas.

- Desarrollar una interfaz de comunicación tipo REST API, que facilite tanto a 
  los usuarios finales, como a otras aplicaciones y servicios internos de la 
  empresa el acceso a la información disponible en la base de datos.

## Supuesto teórico

Se desea desarrollar una base de datos para una empresa que tiene diferentes 
supermercados. Esta base de datos ha de almacenar la información necesaria para
llevar un control de los productos que hay en cada una de las tiendas, de las 
cuales conocemos su identificador, dirección y superficie. 

Debemos almacenar de cada producto información de interés como el identificador
del producto, el nombre, el distribuidor, la marca, el precio, la descripcción,
la categoría ('Alimentacion', 'Limpieza', 'Higiene', 'Textil', 'Herramientas' y
'Otros') y la fecha de caducidad para algunos de ellos.

De igual manera de quiere llevar un control de la contratacion de los empleados, guardando su 
información personal (DNI, nombre, apellidos, dirección, salario, horario de entrada y salida, 
número de cuenta y rol dentro de la tienda (Cajero, Charcuteria, Logistica, Gerente, Pescaderia, 
Carniceria), periodo y destinación. Cabe resaltar que el rol nos servirá para mantener almacenado 
información de algunos roles en específicos, sientos estas las herramientas que usen, para poder 
llevar un control de las herramientas asignadas a cada uno, como puede ser a los encargados del 
almacén los montacargas de cada uno.

Cabe resaltar que cada tienda tiene un único almacen, y deberemos poder almacenar la información de 
la superficie, la temperatura y el empleado que se encarga de este. También tendremos que guardar 
el identificador de la tienda a la que pertenece cada almacén y el stock de cada producto en cada 
almacén, así como tambíen queremos saber la cantidad de cada producto en exposición.

La empresa desea implementar un sistema de fidelización de clientes, por lo que queremos almacenar
la información de los clientes, siendo esta DNI, nombre, apellido, correo, teléfono, dirección y
un descuento que se le aplica a los clientes que realicen compras superiores a 100€ mensuales.

Por último, la empresa quiere llevar un control de las transacciones que se realizan en cada una de
las tiendas, almacenando el identificador del cliente que la ha realizado, el cajero que ha 
gestionado la compra, los productos comprados, el importe total, un identificador de la compra y la 
fecha de la misma. Todo esto servirá a su vez para aplicar el sistemas de descuento a los clientes 
que en caso de que realizen compras de más de 100 euros mensuales, se les aplicará un descuento de
10€ en su próxima compra superior a 50€.

## Modelo entidad-relación

![Modelo entidad-relación](./img/DiagramaER.png)

## Modelo relacional

Cliente (**DNI_CLI**, Nombre, Apellidos, Correo, Telefono, Calle, Ciudad, Provincia, ~~Descuento~~)

---

Producto (**ID_PROD**, Nombre, Distribuidor, Marca, Precio, Descripción, Categoría, FechaCaducidad)

---

Empleado(**DNI_EMP**, Nombre, Apellidos, Calle, Ciudad, Provincia, Salario, HoraEntrada, HoraSalida, NumCuenta, rol)

---

Cajero(***DNI_EMP***, Caja)<br>

Foreing Key (DNI_EMP) references Empleado(DNI_EMP)

---

Charcutería(***DNI_EMP***, Cortadora)<br>

Foreing Key (DNI_EMP) references Empleado(DNI_EMP)

---

Logistica(***DNI_EMP***, Montagarcas)<br>

Foreing Key (DNI_EMP) references Empleado(DNI_EMP)

---

Tienda(**ID_TIE**, Calle, Ciudad, Provincia, Superficie)

---

Almacen(***ID_ALM***, Temperatura, Superficie, *ID_SUPER*)<br>

Foreing Key (ID_ALM) references Tienda(ID_TIE)

Foreing Key (ID_SUPER) references Empleado(DNI_EMP)

---

Trabaja(***DNI_EMP***, ***ID_TIE***, **FechaInicio**, FechaFin)<br>

Foreing Key (DNI_EMP) references Empleado(DNI_EMP)<br>

Foreing Key (ID_TIE) references Tienda(ID_TIE)

---

DisponibilidadTienda(***ID_TIE***, ***ID_PROD***, Cantidad)<br>

Foreing Key (ID_TIE) references Tienda(ID_TIE)<br>

Foreing Key (ID_PROD) references Producto(ID_PROD)

---

DisponibilidadAlmacen(***ID_ALM***, ***ID_PROD***, Cantidad)<br>

Foreing Key (ID_ALM) references Almacen(ID_ALM)<br>

Foreing Key (ID_PROD) references Producto(ID_PROD)

---

Compra(**ID_COMP**)

---

Transaccion(**ID_TRANS**, *DNI_CLI*, *DNI_EMP**, *ID_TIE**, *ID_COMP*, ~~Importe~~, Fecha)<br>

Foreing Key (DNI_CLI) references Cliente(DNI_CLI)

Foreing Key (DNI_EMP) references Empleado(DNI_EMP)

Foreing Key (ID_TIE) references Tienda(ID_TIE)<br>

Foreing Key (ID_COMP) references Compra(ID_COMP)

---

Carrito(***ID_COMP***, ***ID_PROD***, Cantidad)

Foreing Key (ID_COMP) references Compra(ID_COMP)

Foreing Key (ID_PROD) references Producto(ID_PROD)


## Restricciones semánticas

- Tanto el precio de un producto, la cantidad de producto disponible, la superficie de un edificio, como el importe de una transacción deben ser positivos.

- El descuento de un cliente se ubica en el intervalo 0-25%

- El identificador de una máquina no puede ser negativo.

- La fecha de finalización debe ser posterior a la facha de inicio en un periodo laboral.

- El salario mínimo en la compañía es 900€.

- Sólo puede haber un almacén por cada tienda.

- Un empleado de logística puede supervisar un almacén, siempre y cuando haya trabajado en esa tienda alguna vez.

- El descuento de 10€ se aplica para clientes cuyo gasto total supere 100€, en este último mes.

- El importe de una transacción, se calcula en base al precio y la cantidad de los productos de la cesta.

- En una transacción, no se puede comprar un producto que no esté en esa tienda.

- En una transacción, debe atendernos un empleado de caja, que trabaje en dicha tienda.


## Consultas de prueba

Valor total de los productos almacenados por cada tienda.
```sql
SELECT ID_TIE, SUM(Cantidad * Precio) AS valor
FROM DisponibilidadTienda JOIN Producto USING (ID_PROD)
GROUP BY ID_TIE
ORDER BY valor DESC;
```

Añadimos 2 unidades del producto 4 y 1 unidad del producto 2 a la tienda T007.
```sql
INSERT INTO DisponibilidadTienda VALUES
('T007', 4, 2),
('T007', 2, 1);
```

Hacemos una compra (productos 2 y 4) superior a 100€.
```sql
INSERT INTO Compra VALUES (2000);

INSERT INTO Carrito VALUES
(2000, 4, 1),
(2000, 2, 1);

INSERT INTO Transaccion
VALUES (DEFAULT, '55555555G', '12345684G', 'T007', 2000);
```

El cliente ya dispone de un descuento de 10€.
```sql
SELECT Descuento FROM Cliente WHERE DNI_CLI = '55555555G';
```

```sql
SELECT Precio FROM Producto WHERE ID_PROD = 4;
```

Veamos si en la siguiente compra se aplica el descuento.
```sql
INSERT INTO Compra VALUES (3030);

INSERT INTO Carrito VALUES (3030, 4, 1);

INSERT INTO Transaccion
VALUES (5050, '55555555G', '12345684G', 'T007', 3030);

SELECT Importe FROM Transaccion WHERE ID_TRANS = 5050;
```
