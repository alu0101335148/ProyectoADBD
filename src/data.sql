-- Script para cargar los datos iniciales.

-- Inserción de datos para los clientes
INSERT INTO Cliente VALUES ('12345678A', 'Juan', 'Perez', '346404646', 'Calle 1', 'Ciudad 1', 'Provincia 1', 0.1);
INSERT INTO Cliente VALUES ('87654321B', 'Pepe', 'Garcia', '346656766', 'Calle 2', 'Ciudad 2', 'Provincia 2', 0.2);
INSERT INTO Cliente VALUES ('11111111C', 'Maria', 'Gonzalez', '646886861', 'Calle 3', 'Ciudad 3', 'Provincia 3', 0.3);
INSERT INTO Cliente VALUES ('22222222D', 'Luis', 'Rodriguez', '122678646', 'Calle 4', 'Ciudad 4', 'Provincia 4', 0.4);
INSERT INTO Cliente VALUES ('33333333E', 'Ana', 'Martinez', '562163336', 'Calle 5', 'Ciudad 5', 'Provincia 5', 0.5);
INSERT INTO Cliente VALUES ('44444444F', 'Jose', 'Lopez', '232362366', 'Calle 6', 'Ciudad 6', 'Provincia 6', 0.6);
INSERT INTO Cliente VALUES ('55555555G', 'Laura', 'Sanchez', '969699626', 'Calle 7', 'Ciudad 7', 'Provincia 7', 0.7);

-- Insertar datos para los productos
-- CREATE TABLE Producto(
--     ID_PROD SERIAL PRIMARY KEY,
--     Nombre VARCHAR(30) NOT NULL,
--     Distribuidor VARCHAR(30) NOT NULL,
--     Marca VARCHAR(30) NOT NULL,
--     Precio FLOAT NOT NULL,
--     Descripcion VARCHAR(150) NOT NULL,
--     Categoria CATEGORIAS NOT NULL,
--     FechaCaducidad DATE
-- );
INSERT INTO Producto VALUES (DEFAULT, 'Crema hidratante', 'Distribuidora Cream', 'Soft Skin S.A.', 12.99, 'Crema hidratante para piel seca y sensible', 'Higiene', '2023-01-31');
INSERT INTO Producto VALUES (DEFAULT, 'Sábanas de algodón', 'Distribuidora Sheets', 'Comfy Bedding S.L.', 24.99, 'Sábanas suaves y cómodas de algodón 100%', 'Textil', NULL);
INSERT INTO Producto VALUES (DEFAULT, 'Bolsa de deporte', 'Distribuidora Sport', 'Fit Gear S.A.', 29.99, 'Bolsa de deporte grande y resistente con compartimentos especializados', 'Otros', NULL);
INSERT INTO Producto VALUES (DEFAULT, 'Juego de cuchillos de cocina', 'Distribuidora Knives', 'Sharp Blades S.L.', 89.99, 'Juego de cuchillos de cocina de acero inoxidable y mango ergonómico', 'Herramientas', '2023-12-01');
INSERT INTO Producto VALUES (DEFAULT, 'Aceite de oliva', 'Distribuidora Olive', 'Olive Oil S.A.', 3.99, 'Aceite de oliva virgen extra de alta calidad', 'Alimentacion', '2023-05-01');
INSERT INTO Producto VALUES (DEFAULT, 'Limpiador multiusos', 'Distribuidora Cleaner', 'Fresh Home S.L.', 4.99, 'Limpiador multiusos eficaz para todas las superficies', 'Limpieza', NULL);
INSERT INTO Producto VALUES (DEFAULT, 'Cepillo de dientes eléctrico', 'Distribuidora Brush', 'Clean Teeth Inc.', 49.99, 'Cepillo de dientes eléctrico con tecnología de limpieza avanzada', 'Higiene', NULL);
INSERT INTO Producto VALUES (DEFAULT, 'Toallas de baño', 'Distribuidora Towels', 'Absorbent Towels S.A.', 9.99, 'Toallas de baño suaves y absorbentes', 'Textil', NULL);
INSERT INTO Producto VALUES (DEFAULT, 'Llave inglesa', 'Distribuidora Wrench', 'Power Tools S.L.', 9.99, 'Llave inglesa resistente y de alta calidad', 'Herramientas', NULL);
INSERT INTO Producto VALUES (DEFAULT, 'Regla metálica', 'Distribuidora Ruler', 'Precise Measures S.A.', 3.99, 'Regla metálica de precisión y durabilidad', 'Otros', NULL);
INSERT INTO Producto VALUES (DEFAULT, 'Arroz integral', 'Distribuidora Rice', 'Healthy Grains S.L.', 2.99, 'Arroz integral 100% natural y sin gluten', 'Alimentacion', '2023-09-01');
INSERT INTO Producto VALUES (DEFAULT, 'Leche desnatada', 'Distribuidora Milk', 'Low Fat Dairy S.A.', 1.99, 'Leche desnatada de vaca de alta calidad y sin grasas añadidas', 'Alimentacion', '2023-01-15');
INSERT INTO Producto VALUES (DEFAULT, 'Jugo de naranja', 'Distribuidora Juice', 'Fresh Squeezed S.L.', 2.49, 'Jugo de naranja 100% natural y sin azúcares añadidos', 'Alimentacion', '2023-04-01');
INSERT INTO Producto VALUES (DEFAULT, 'Galletas integrales', 'Distribuidora Cookies', 'Whole Wheat S.A.', 3.99, 'Galletas integrales de avena y pasas de uva', 'Alimentacion', '2023-02-01');
INSERT INTO Producto VALUES (DEFAULT, 'Cereales integrales', 'Distribuidora Cereal', 'Whole Grains S.L.', 4.99, 'Cereales integrales con frutas y nueces', 'Alimentacion', '2023-07-01');


-- Insertar datos para los empleados
-- CREATE TABLE Empleado(
--     DNI_EMP VARCHAR(9) PRIMARY KEY,
--     Nombre VARCHAR(30) NOT NULL,
--     Apellidos VARCHAR(30) NOT NULL,
--     Calle VARCHAR(30) NOT NULL,
--     Ciudad VARCHAR(30) NOT NULL,
--     Provincia VARCHAR(30) NOT NULL,
--     Salario FLOAT NOT NULL,
--     HoraEntrada TIME NOT NULL,
--     HoraSalida TIME NOT NULL,
--     NumCuenta VARCHAR(30) NOT NULL,
--     Rol PUESTO NOT NULL
-- );
INSERT INTO Empleado VALUES ('12345678A', 'Juan', 'Pérez', 'Calle del Sol', 'Madrid', 'Madrid', 1200, '09:00:00', '17:00:00', '123456781234', 'Cajero');
INSERT INTO Empleado VALUES ('12345679B', 'Ana', 'García', 'Calle de la Luna', 'Barcelona', 'Cataluña', 1400, '08:00:00', '16:00:00', '123456791234', 'Charcuteria');
INSERT INTO Empleado VALUES ('12345680C', 'Pablo', 'Rodríguez', 'Calle del Mar', 'Valencia', 'Valencia', 1600, '09:00:00', '17:00:00', '12345680234', 'Logistica');
INSERT INTO Empleado VALUES ('12345681D', 'Sandra', 'Lopez', 'Calle de las Estrellas', 'Sevilla', 'Andalucía', 1800, '09:00:00', '17:00:00', '12345681234', 'Gerente');
INSERT INTO Empleado VALUES ('12345682E', 'Alberto', 'Fernandez', 'Calle del Rio', 'Zaragoza', 'Aragón', 2000, '09:00:00', '17:00:00', '12345682234', 'Pescaderia');
INSERT INTO Empleado VALUES ('12345683F', 'Laura', 'Martinez', 'Calle de la Montaña', 'Málaga', 'Andalucía', 2200, '09:00:00', '17:00:00', '12345683234', 'Carniceria');
INSERT INTO Empleado VALUES ('12345684G', 'Javier', 'Gonzalez', 'Calle del Cielo', 'Bilbao', 'País Vasco', 2400, '09:00:00', '17:00:00', '12345684234', 'Cajero');
INSERT INTO Empleado VALUES ('12345685H', 'Cristina', 'Ruiz', 'Calle de la Tierra', 'Murcia', 'Murcia', 2600, '09:00:00', '17:00:00', '12345685234', 'Charcuteria');
INSERT INTO Empleado VALUES ('12345686I', 'Raquel', 'Díaz', 'Calle del Sol', 'Barcelona', 'Cataluña', 2800, '09:00:00', '17:00:00', '12345686234', 'Logistica');
INSERT INTO Empleado VALUES ('12345687J', 'Irene', 'Rodriguez', 'Calle de la Luna', 'Madrid', 'Madrid', 3000, '09:00:00', '17:00:00', '12345687234', 'Gerente');


-- Insertar datos para los cajeros
-- CREATE TABLE Cajero(
--     DNI_EMP VARCHAR(9) PRIMARY KEY,
--     Caja INT NOT NULL,
--     FOREIGN KEY (DNI_EMP) REFERENCES Empleado(DNI_EMP) ON DELETE CASCADE
-- );
INSERT INTO Cajero VALUES ('12345684G', 1);
INSERT INTO Cajero VALUES ('12345678A', 1);

-- Insertar datos para los empleados encargados de la charcuteria 
-- CREATE TABLE Charcuteria(
--     DNI_EMP VARCHAR(9) PRIMARY KEY,
--     Cortadora INT NOT NULL,
--     FOREIGN KEY (DNI_EMP) REFERENCES Empleado(DNI_EMP) ON DELETE CASCADE
-- );
INSERT INTO Charcuteria VALUES ('12345679B', 1);
INSERT INTO Charcuteria VALUES ('12345685H', 2);

-- Insertar datos para los empleados encargados de los almacenes
-- CREATE TABLE Logistica(
--     DNI_EMP VARCHAR(9) PRIMARY KEY,
--     Montacargas INT NOT NULL,
--     FOREIGN KEY (DNI_EMP) REFERENCES Empleado(DNI_EMP) ON DELETE CASCADE
-- );
INSERT INTO Logistica VALUES ('12345680C', 2);
INSERT INTO Logistica VALUES ('12345686I', 3);


-- Insertar datos para las tiendas
-- CREATE TABLE Tienda(
--     ID_TIE VARCHAR(30) PRIMARY KEY,
--     Calle VARCHAR(30) NOT NULL,
--     Ciudad VARCHAR(30) NOT NULL,
--     Provincia VARCHAR(30) NOT NULL,
--     Superficie FLOAT NOT NULL
-- );
INSERT INTO Tienda VALUES ('T001', 'Calle de la Paz', 'Madrid', 'Madrid', 200);
INSERT INTO Tienda VALUES ('T002', 'Calle del Sol', 'Barcelona', 'Cataluña', 300);
INSERT INTO Tienda VALUES ('T003', 'Calle de la Luna', 'Valencia', 'Comunidad Valenciana', 250);
INSERT INTO Tienda VALUES ('T004', 'Calle de las Estrellas', 'Sevilla', 'Andalucía', 350);
INSERT INTO Tienda VALUES ('T005', 'Calle del Mar', 'Málaga', 'Andalucía', 400);
INSERT INTO Tienda VALUES ('T006', 'Calle de la Montaña', 'Bilbao', 'País Vasco', 300);
INSERT INTO Tienda VALUES ('T007', 'Calle del Río', 'Zaragoza', 'Aragón', 250);
INSERT INTO Tienda VALUES ('T008', 'Calle del Bosque', 'Mallorca', 'Islas Balears', 350);
INSERT INTO Tienda VALUES ('T009', 'Calle de la Pradera', 'Granada', 'Andalucía', 400);
INSERT INTO Tienda VALUES ('T010', 'Calle del Desierto', 'Tenerife', 'Islas Canarias', 350);

-- Insertar datos para la tabla trabaja
-- CREATE TABLE Trabaja(
--     DNI_EMP VARCHAR(9),
--     ID_TIE VARCHAR(30),
--     FechaInicio DATE,
--     FechaFin DATE,
--     FOREIGN KEY (DNI_EMP) REFERENCES Empleado(DNI_EMP) ON DELETE CASCADE,
--     FOREIGN KEY (ID_TIE) REFERENCES Tienda(ID_TIE) ON DELETE CASCADE,
--     PRIMARY KEY (DNI_EMP, ID_TIE, FechaInicio)
-- );
INSERT INTO Trabaja VALUES ('12345678A', 'T001', '2020-01-01', NULL);
INSERT INTO Trabaja VALUES ('12345679B', 'T002', '2020-02-01', '2020-07-31');
INSERT INTO Trabaja VALUES ('12345680C', 'T003', '2020-03-01', NULL);
INSERT INTO Trabaja VALUES ('12345681D', 'T004', '2020-04-01', '2020-09-30');
INSERT INTO Trabaja VALUES ('12345682E', 'T005', '2020-05-01', '2020-10-31');
INSERT INTO Trabaja VALUES ('12345683F', 'T006', '2020-06-01', '2020-11-30');
INSERT INTO Trabaja VALUES ('12345684G', 'T007', '2020-07-01', NULL);
INSERT INTO Trabaja VALUES ('12345685H', 'T008', '2020-08-01', '2021-01-31');
INSERT INTO Trabaja VALUES ('12345686I', 'T009', '2020-09-01', '2020-10-01');
INSERT INTO Trabaja VALUES ('12345686I', 'T009', '2020-10-01', NULL);
INSERT INTO Trabaja VALUES ('12345687J', 'T010', '2020-10-01', '2021-03-31');
INSERT INTO Trabaja VALUES ('12345687J', 'T010', '2021-04-29', NULL);

-- Insertar datos para los almacenes
-- CREATE TABLE Almacen(
--     ID_ALM VARCHAR(30) PRIMARY KEY,
--     Temperatura FLOAT NOT NULL,
--     Superficie FLOAT NOT NULL,
--     ID_EMP VARCHAR(9),
--     FOREIGN KEY (ID_ALM) REFERENCES Tienda(ID_TIE) ON DELETE CASCADE,
--     FOREIGN KEY (ID_EMP) REFERENCES Empleado(DNI_EMP) ON DELETE SET NULL
-- );
INSERT INTO Almacen VALUES ('T001', 18, 500, '12345678A');
INSERT INTO Almacen VALUES ('T002', 20, 700, '12345679B');
INSERT INTO Almacen VALUES ('T003', 22, 400, '12345680C');
INSERT INTO Almacen VALUES ('T004', 24, 1000, '12345681D');
INSERT INTO Almacen VALUES ('T005', 18, 800, '12345682E');
INSERT INTO Almacen VALUES ('T006', 20, 900, '12345683F');
INSERT INTO Almacen VALUES ('T007', 22, 700, '12345684G');
INSERT INTO Almacen VALUES ('T008', 24, 1200, '12345685H');
INSERT INTO Almacen VALUES ('T009', 18, 1000, '12345686I');
INSERT INTO Almacen VALUES ('T010', 20, 1200, '12345687J');

-- Insertar datos para la tabla DisponibilidadTienda
-- CREATE TABLE DisponibilidadTienda(
--     ID_TIE VARCHAR(30),
--     ID_PROD INT,
--     Cantidad INT NOT NULL,
--     FOREIGN KEY (ID_TIE) REFERENCES Tienda(ID_TIE) ON DELETE CASCADE,
--     FOREIGN KEY (ID_PROD) REFERENCES Producto(ID_PROD) ON DELETE CASCADE,
--     PRIMARY KEY (ID_TIE, ID_PROD)
-- );
INSERT INTO DisponibilidadTienda VALUES
('T001', 1, 7),
('T001', 2, 8),
('T002', 3, 9),
('T002', 4, 10),
('T002', 5, 6),
('T003', 2, 5),
('T004', 1, 3),
('T004', 3, 2),
('T004', 5, 8),
('T005', 4, 1),
('T006', 2, 9),
('T007', 1, 7),
('T007', 3, 4),
('T008', 2, 6),
('T008', 4, 3),
('T009', 1, 2),
('T009', 5, 5),
('T010', 3, 8);

-- Insertar datos para la tabla DisponibilidadAlmacen
-- CREATE TABLE DisponibilidadAlmacen(
--     ID_ALM VARCHAR(30),
--     ID_PROD INT,
--     Cantidad INT NOT NULL,
--     FOREIGN KEY (ID_ALM) REFERENCES Almacen(ID_ALM) ON DELETE CASCADE,
--     FOREIGN KEY (ID_PROD) REFERENCES Producto(ID_PROD) ON DELETE CASCADE,
--     PRIMARY KEY (ID_ALM, ID_PROD)
-- );
INSERT INTO DisponibilidadAlmacen VALUES ('T001', 1, 10);
INSERT INTO DisponibilidadAlmacen VALUES ('T001', 2, 20);
INSERT INTO DisponibilidadAlmacen VALUES ('T002', 3, 30);
INSERT INTO DisponibilidadAlmacen VALUES ('T002', 4, 40);
INSERT INTO DisponibilidadAlmacen VALUES ('T003', 5, 50);
INSERT INTO DisponibilidadAlmacen VALUES ('T003', 6, 60);
INSERT INTO DisponibilidadAlmacen VALUES ('T004', 7, 70);
INSERT INTO DisponibilidadAlmacen VALUES ('T004', 8, 80);
INSERT INTO DisponibilidadAlmacen VALUES ('T005', 9, 90);
INSERT INTO DisponibilidadAlmacen VALUES ('T005', 10, 100);

-- Insertar datos para la tabla Compra
INSERT INTO Compra VALUES (DEFAULT);
INSERT INTO Compra VALUES (DEFAULT);
INSERT INTO Compra VALUES (DEFAULT);

-- Insertar datos para la tabla Carrito
-- CREATE TABLE Carrito(
--     ID_COMP INT,
--     ID_PROD INT,
--     Cantidad INT NOT NULL,
--     FOREIGN KEY (ID_PROD) REFERENCES Producto(ID_PROD) ON DELETE CASCADE,
--     PRIMARY KEY (ID_COMP, ID_PROD)
-- );
INSERT INTO Carrito VALUES (1, 11, 1);
INSERT INTO Carrito VALUES (1, 12, 2);
INSERT INTO Carrito VALUES (1, 13, 3);
INSERT INTO Carrito VALUES (1, 14, 4);
INSERT INTO Carrito VALUES (2, 15, 15);
INSERT INTO Carrito VALUES (2, 16, 10);
INSERT INTO Carrito VALUES (2, 17, 7);
INSERT INTO Carrito VALUES (3, 18, 8);
INSERT INTO Carrito VALUES (3, 19, 1);
INSERT INTO Carrito VALUES (3, 20, 2);

-- Insertar datos para la tabla Transaccion
-- CREATE TABLE Transaccion(
--     ID_TRANS SERIAL PRIMARY KEY,
--     DNI_CLI VARCHAR(9),
--     DNI_EMP VARCHAR(9),
--     ID_TIE VARCHAR(30),
--     Importe FLOAT NOT NULL,
--     Fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
--     FOREIGN KEY (DNI_CLI) REFERENCES Cliente(DNI_CLI) ON DELETE SET NULL,
--     FOREIGN KEY (DNI_EMP) REFERENCES Empleado(DNI_EMP) ON DELETE SET NULL,
--     FOREIGN KEY (ID_TIE) REFERENCES Tienda(ID_TIE) ON DELETE SET NULL
-- );
INSERT INTO Transaccion VALUES (DEFAULT, '12345681D', '12345678A', 'T001');
INSERT INTO Transaccion VALUES (DEFAULT, '12345682E', '12345678A', 'T001');
INSERT INTO Transaccion VALUES (DEFAULT, '12345683F', '12345678A', 'T001');
-- INSERT INTO Transaccion VALUES (DEFAULT, DEFAULT, '12345684G', '12345678A', 'T005', 20);
-- INSERT INTO Transaccion VALUES (DEFAULT, DEFAULT, '12345685H', '12345678A', 'T006', 10);
-- INSERT INTO Transaccion VALUES (DEFAULT, DEFAULT, '12345686I', '12345678A', 'T007', 70.5);
-- INSERT INTO Transaccion VALUES (DEFAULT, DEFAULT, '12345687J', '12345678A', 'T008', 13.3);
-- INSERT INTO Transaccion VALUES (DEFAULT, DEFAULT, '12345678A', '12345678A', 'T009', 9);
