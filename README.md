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

- Actualización automática del stock de las tiendas, tras realizar una compra.

- Aplicación automática de descuentos a ciertos clientes.

- Tener un sistema preventor de inserción de consultas erróneas (precios negativos, saldos por debajo del salario mínimo, etc).

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

De igual manera se quiere llevar un control de la contratación de los empleados, 
guardando su información personal (DNI, nombre, apellidos, dirección, salario, 
horario de entrada y salida, número de cuenta y rol dentro de la tienda (Cajero, 
Charcuteria, Logistica, Gerente, Pescaderia, Carniceria), periodo y destinación.
Cabe resaltar que el rol nos servirá para mantener almacenado información de 
algunos puestos específicos, como las herramientas que usen, para poder llevar 
un control de las herramientas asignadas a cada uno, como puede ser a los 
encargados del almacén los montacargas de cada uno.

Cabe resaltar que cada tienda tiene un único almacen, y deberemos poder 
almacenar la información de la superficie, la temperatura y el empleado que se 
encarga de este. También tendremos que guardar el identificador de la tienda a 
la que pertenece cada almacén y el stock de cada producto en cada  almacén, así 
como tambíen queremos saber la cantidad de cada producto en exposición.

La empresa desea implementar un sistema de fidelización de clientes, por lo que
queremos almacenar la información de los clientes, siendo esta DNI, nombre, 
apellido, correo, teléfono, dirección y un descuento que se le aplica a los 
clientes que realicen compras superiores a 100€ mensuales.

Por último, la empresa quiere llevar un control de las transacciones que se 
realizan en cada una de las tiendas, almacenando el identificador del cliente 
que la ha realizado, el cajero que ha  gestionado la compra, los productos 
comprados, el importe total, un identificador de la compra y la fecha de la 
misma. Todo esto servirá a su vez para aplicar el sistema de descuento a los 
clientes que en caso de que realizen compras de más de 100 euros mensuales, se 
les aplicará un descuento de 10€ en su próxima compra superior a 50€.

## Modelo entidad-relación

![Modelo entidad-relación](./img/DiagramaER.png)

De cara a las decisiones fundamentales de nuestro diseño las vamos a dividir en 
diferentes secciones: la gestion de los empleados, la gestion de los productos, 
y la la gestion de los clientes y las transacciones.

### Gestión de empleados

![Modelo Empleados](./img/Empleados.png)

Como se nos estipula en el supuesto teórico, vamos a tener que almacenar cierta 
información de los empleados, de ahí que creemos dicha entidad, no obstante 
como se nos menciona que dependiendo del rol de estos, se almacenará la 
herramienta que tengan asignada, que no siempre existirá, se optó por hacer una 
implementación de herencia, guardando en diferentes tablas simplemente dicha 
información.

Por otro lado también vamos a tener que guardar un registro de las 
destinaciones de cada empleado y como debemos tener una entidad tienda para 
almacenar la información de interés de cada una de las tiendas de forma 
independiente, simplemente los relacionamos mediante una relación de trabaja, 
que derivará posteriormente en una tabla.

Finalmente se optó por una relación de supervisión entre los almacenes 
(específicos de cada tienda en una relación de 1 a 1), con los empleados de 
logística, debido a que necesitamos que los almacenes tengan un supervisor.

### Gestión de stock

![Almacen](img/Almacen.png)

Para la gestión de los productos en cada tienda, partimos de 3 entidades 
básicas, la tienda, el producto, y el almacén. Estas entidades optamos por 
unirlas con relaciones de "dispone" y "producto en", de esta forma 
almacenaremos el stock expuesto en tienda y el stock en el almacén para cada
una de los supermercados.

Cabe resaltar que almacén es una entidad débil, debido a que cada almacén está
ligado a una tienda en una relación 1 a 1 de pertenencia, por lo que si 
desaparece la tienda debería desaparecer el almacén.

### Gestión de clientes y transacciones

![Modelo Clientes](./img/Transacciones.png)

Con respecto a los clientes, éstos se representan como una entidad propia y se
recogen diversos atributos. Los clientes pueden recibir descuentos en función
de su volumen de gasto mensual, por ello dicho atributo debe ser calculado
posteriormente.

Como se ha comentado al inicio, las transacciones realizadas en las tiendas son
un aspecto central del negocio y de nuestro diseño. Éstas se representan como una
relación múltiple, que asocia 4 entidades fundamentales:
- Cliente, cardinalidad N. Es el cliente que realiza la compra.
- Empleado (puesto de caja), cardinalidad N. Atiende al cliente.
- Tienda, cardinalidad N. Lugar dónde se realiza la compra.
- Compra, cardinalidad 1. Representa los productos comprados.

Cabe destacar que el importe monetario total, se calcula automáticamente en base
al contenido del carrito y los precios de los productos.

Por tanto, cada transacción debe hacer referencia a un conjunto de productos
(las compras individuales suelen ser poco comunes), esto es posible gracias
a una entidad auxiliar llamada `Compra`, de lo contrario, no podríamos hacer
referencia a la entidad `Carrito` a través de una clave ajena, pues el atributo
referenciado debe ser una clave primaria (por tanto única) en la otra entidad.

Finalmente, la entidad `Carrito`, contiene los (posiblemente múltiples) productos
de una compra, así como las cantidades adquiridas para cada uno. Es necesario
relacionarse con la entidad `Producto`, para poder obtener su precio.

## Modelo relacional

![Modelo relacional](./img/ModeloRelacional.png)

## Grafo relacional

![Grafo relacional](./img/ERDBeaver.png)

## Restricciones semánticas

- Tanto el precio de un producto, la cantidad de producto disponible, la 
  superficie de un edificio, como el importe de una transacción deben ser 
  positivos.

- El descuento de un cliente se ubica en el intervalo 0-25%

- El identificador de una máquina no puede ser negativo.

- La fecha de finalización debe ser posterior a la facha de inicio en un 
  periodo laboral.

- El salario mínimo en la compañía es 900€.

- Sólo puede haber un almacén por cada tienda.

- Un empleado de logística puede supervisar un almacén, siempre y cuando haya 
  trabajado en esa tienda alguna vez.

- El descuento de 10€ se aplica para clientes cuyo gasto total supere 100€, en 
  este último mes.

- El importe de una transacción, se calcula en base al precio y la cantidad de 
  los productos de la cesta.

- Todos los productos de una compra, deben estar disponibles en la tienda con 
  suficiente cantidad.

- En una transacción, no se puede comprar un producto que no esté en esa tienda.

- En una transacción, debe atendernos un empleado de caja, que trabaje en dicha 
  tienda.


## Consultas de prueba

Valor total de los productos almacenados por cada tienda.
```sql
SELECT ID_TIE, SUM(Cantidad * Precio) AS valor
FROM DisponibilidadTienda JOIN Producto USING (ID_PROD)
GROUP BY ID_TIE
ORDER BY valor DESC;
```

```
 id_tie |       valor        
--------+--------------------
 T001   |  4849.429999999999
 T002   | 1549.9199999999998
 T003   |             427.74
 T008   | 419.90999999999997
 T010   |             239.92
 T006   |             224.91
 T005   |              89.99
 T004   |              79.93
 T007   |              49.95
 T009   |  45.93000000000001
(10 rows)
```

Añadimos 2 unidades del producto 4 y 1 unidad del producto 2 a la tienda T007.
```sql
INSERT INTO DisponibilidadTienda VALUES
('T007', 4, 2),
('T007', 2, 1);
```

```
 id_tie | id_prod | cantidad 
--------+---------+----------
 T007   |       4 |        2
 T007   |       2 |        1
(2 rows)
```

Hacemos una compra (productos 2 y 4) superior a 100€.
```sql
SELECT Precio FROM Producto WHERE ID_PROD IN (1, 4);
```



```sql
INSERT INTO Compra VALUES (2000);

INSERT INTO Carrito VALUES
(2000, 4, 1),
(2000, 2, 1);

INSERT INTO Transaccion
VALUES (DEFAULT, '12345678A', '87654321A', 'T001', 2000);
```

El cliente ya dispone de un descuento de 10€.
```sql
SELECT Descuento FROM Cliente WHERE DNI_CLI = '12345678A';
```

Veamos si en la siguiente compra se aplica el descuento.
```sql
INSERT INTO Compra VALUES (3030);

INSERT INTO Carrito VALUES (3030, 4, 1);

INSERT INTO Transaccion
VALUES (5050, '12345678A', '87654321A', 'T001', 3030);

SELECT Importe FROM Transaccion WHERE ID_TRANS = 5050;
```

Por otra parte,
