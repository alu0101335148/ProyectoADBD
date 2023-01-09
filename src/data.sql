-- Script para cargar los datos iniciales.

INSERT INTO Cliente VALUES 
('12345678A', 'Juan', 'Perez', 'JuanPerez@gmail.com', '346404646', 'Calle 1', 'Ciudad 1', 'Provincia 1'),
('12345678B', 'Pepe', 'Garcia', 'PepeGarcia@gmail.com', '346656766', 'Calle 2', 'Ciudad 2', 'Provincia 2'),
('12345678C', 'Maria', 'Gonzalez', 'MariaGonzalez@gmail.com', '646886861', 'Calle 3', 'Ciudad 3', 'Provincia 3'),
('12345678D', 'Luis', 'Rodriguez', NULL, '122678646', 'Calle 4', 'Ciudad 4', 'Provincia 4'),
('12345678E', 'Ana', 'Martinez', NULL, '562163336', 'Calle 5', 'Ciudad 5', 'Provincia 5'),
('12345678F', 'Jose', 'Lopez', NULL, '232362366', 'Calle 6', 'Ciudad 6', 'Provincia 6'),
('12345678G', 'Laura', 'Sanchez', NULL, '969699626', 'Calle 7', 'Ciudad 7', 'Provincia 7'),
('12345678H', 'Antonio', 'Fernandez', NULL, '346404646', 'Calle 8', 'Ciudad 8', 'Provincia 8');



INSERT INTO Producto VALUES 
(DEFAULT, 'Crema hidratante', 'Distribuidora Cream', 'Soft Skin S.A.', 12.99, 'Crema hidratante para piel seca y sensible', 'Higiene', '2023-01-31'),
(DEFAULT, 'Sábanas de algodón', 'Distribuidora Sheets', 'Comfy Bedding S.L.', 24.99, 'Sábanas suaves y cómodas de algodón 100%', 'Textil', NULL),
(DEFAULT, 'Bolsa de deporte', 'Distribuidora Sport', 'Fit Gear S.A.', 29.99, 'Bolsa de deporte grande y resistente con compartimentos especializados', 'Otros', NULL),
(DEFAULT, 'Juego de cuchillos de cocina', 'Distribuidora Knives', 'Sharp Blades S.L.', 89.99, 'Juego de cuchillos de cocina de acero inoxidable y mango ergonómico', 'Herramientas', '2023-12-01'),
(DEFAULT, 'Aceite de oliva', 'Distribuidora Olive', 'Olive Oil S.A.', 3.99, 'Aceite de oliva virgen extra de alta calidad', 'Alimentacion', '2023-05-01'),
(DEFAULT, 'Limpiador multiusos', 'Distribuidora Cleaner', 'Fresh Home S.L.', 4.99, 'Limpiador multiusos eficaz para todas las superficies', 'Limpieza', NULL),
(DEFAULT, 'Cepillo de dientes eléctrico', 'Distribuidora Brush', 'Clean Teeth Inc.', 49.99, 'Cepillo de dientes eléctrico con tecnología de limpieza avanzada', 'Higiene', NULL),
(DEFAULT, 'Toallas de baño', 'Distribuidora Towels', 'Absorbent Towels S.A.', 9.99, 'Toallas de baño suaves y absorbentes', 'Textil', NULL),
(DEFAULT, 'Llave inglesa', 'Distribuidora Wrench', 'Power Tools S.L.', 9.99, 'Llave inglesa resistente y de alta calidad', 'Herramientas', NULL),
(DEFAULT, 'Regla metálica', 'Distribuidora Ruler', 'Precise Measures S.A.', 3.99, 'Regla metálica de precisión y durabilidad', 'Otros', NULL),
(DEFAULT, 'Arroz integral', 'Distribuidora Rice', 'Healthy Grains S.L.', 2.99, 'Arroz integral 100% natural y sin gluten', 'Alimentacion', '2023-09-01'),
(DEFAULT, 'Leche desnatada', 'Distribuidora Milk', 'Low Fat Dairy S.A.', 1.99, 'Leche desnatada de vaca de alta calidad y sin grasas añadidas', 'Alimentacion', '2023-01-15'),
(DEFAULT, 'Jugo de naranja', 'Distribuidora Juice', 'Fresh Squeezed S.L.', 2.49, 'Jugo de naranja 100% natural y sin azúcares añadidos', 'Alimentacion', '2023-04-01'),
(DEFAULT, 'Galletas integrales', 'Distribuidora Cookies', 'Whole Wheat S.A.', 3.99, 'Galletas integrales de avena y pasas de uva', 'Alimentacion', '2023-02-01'),
(DEFAULT, 'Cereales integrales', 'Distribuidora Cereal', 'Whole Grains S.L.', 4.99, 'Cereales integrales con frutas y nueces', 'Alimentacion', '2023-07-01');



INSERT INTO Empleado VALUES
('87654321A', 'Juan', 'Pérez', 'Calle del Sol', 'Madrid', 'Madrid', 1200, '09:00:00', '17:00:00', '123456781234', 'Cajero'),
('87654321B', 'Ana', 'García', 'Calle de la Luna', 'Barcelona', 'Cataluña', 1400, '08:00:00', '16:00:00', '123456791234', 'Cajero'),
('87654321C', 'Pablo', 'Rodríguez', 'Calle del Mar', 'Valencia', 'Valencia', 1600, '09:00:00', '17:00:00', '12345680234', 'Cajero'),
('87654321D', 'Sandra', 'Lopez', 'Calle de las Estrellas', 'Sevilla', 'Andalucía', 1800, '09:00:00', '17:00:00', '12345681234', 'Cajero'),
('87654321E', 'Alberto', 'Fernandez', 'Calle del Rio', 'Zaragoza', 'Aragón', 2000, '09:00:00', '17:00:00', '12345682234', 'Charcuteria'),
('87654321F', 'Laura', 'Martinez', 'Calle de la Montaña', 'Málaga', 'Andalucía', 2200, '09:00:00', '17:00:00', '12345683234', 'Charcuteria'),
('87654321G', 'Javier', 'Gonzalez', 'Calle del Cielo', 'Bilbao', 'País Vasco', 2400, '09:00:00', '17:00:00', '12345684234', 'Logistica'),
('87654321H', 'Cristina', 'Ruiz', 'Calle de la Tierra', 'Murcia', 'Murcia', 2600, '09:00:00', '17:00:00', '12345685234', 'Logistica'),
('87654321I', 'Raquel', 'Díaz', 'Calle del Sol', 'Barcelona', 'Cataluña', 2800, '09:00:00', '17:00:00', '12345686234', 'Logistica'),
('87654321J', 'Irene', 'Rodriguez', 'Calle de la Luna', 'Madrid', 'Madrid', 3000, '09:00:00', '17:00:00', '12345687234', 'Gerente'),
('87654321K', 'Manuel', 'Castilla', 'Calle Castro', 'La Laguna', 'Santa Cruz de Tenerife', 3000, '09:00:00', '17:00:00', '12345687234', 'Pescaderia'),
('87654321L', 'Maria', 'Sanchez', 'Calle Palomar', 'A Coruña', 'Galicia', 3000, '09:00:00', '17:00:00', '43253234534', 'Carniceria');



INSERT INTO Cajero VALUES 
('87654321A', 1),
('87654321B', 2),
('87654321C', 3),
('87654321D', 1);



INSERT INTO Charcuteria VALUES 
('87654321E', 1),
('87654321F', 2);



INSERT INTO Logistica VALUES
('87654321G', 1),
('87654321H', 1),
('87654321I', 4);



INSERT INTO Tienda VALUES 
('T001', 'Calle de la Paz', 'Madrid', 'Madrid', 200),
('T002', 'Calle del Sol', 'Barcelona', 'Cataluña', 300),
('T003', 'Calle de la Luna', 'Valencia', 'Comunidad Valenciana', 250),
('T004', 'Calle de las Estrellas', 'Sevilla', 'Andalucía', 350),
('T005', 'Calle del Mar', 'Málaga', 'Andalucía', 400),
('T006', 'Calle de la Montaña', 'Bilbao', 'País Vasco', 300),
('T007', 'Calle del Río', 'Zaragoza', 'Aragón', 250),
('T008', 'Calle del Bosque', 'Mallorca', 'Islas Balears', 350),
('T009', 'Calle de la Pradera', 'Granada', 'Andalucía', 400),
('T010', 'Calle del Desierto', 'Tenerife', 'Islas Canarias', 350);



INSERT INTO Trabaja VALUES
('87654321A', 'T001', '2019-01-01', '2019-02-01'),
('87654321A', 'T001', '2020-01-01', NULL),
('87654321B', 'T007', '2019-01-04', '2019-02-27'),
('87654321B', 'T002', '2020-02-01', '2020-07-31'),
('87654321C', 'T003', '2020-03-01', NULL),
('87654321D', 'T004', '2020-04-01', '2020-09-30'),
('87654321E', 'T001', '2020-05-01', '2020-10-31'),
('87654321F', 'T002', '2020-06-01', '2020-11-30'),
('87654321G', 'T001', '2020-07-01', NULL),
('87654321H', 'T002', '2020-08-01', '2021-01-31'),
('87654321I', 'T003', '2020-09-01', '2020-10-01'),
('87654321J', 'T001', '2020-10-01', NULL),
('87654321K', 'T001', '2020-10-01', '2021-03-31'),
('87654321L', 'T001', '2021-04-29', NULL);



INSERT INTO Almacen VALUES
('T001', 18, 500, '87654321G'),
('T002', -2, 700, '87654321H'),
('T003', 0, 400, '87654321I'),
('T004', 24, 1000, NULL),
('T005', 18, 800, NULL),
('T006', 20, 900, NULL),
('T007', 22, 700, NULL),
('T008', 24, 1200, NULL),
('T009', 18, 1000, NULL),
('T010', 20, 1200, NULL);



INSERT INTO DisponibilidadTienda VALUES
('T001', 1, 7),
('T001', 2, 8),
('T001', 3, 12),
('T001', 4, 43),
('T001', 5, 42),
('T001', 6, 31),
('T001', 7, 4),
('T001', 8, 9),
('T001', 9, 1),
('T001', 10, 42),
('T001', 11, 16),
('T001', 12, 15),
('T001', 13, 20),
('T001', 14, 31),
('T001', 15, 11),
('T002', 3, 9),
('T002', 4, 10),
('T002', 5, 12),
('T002', 8, 32),
('T002', 9, 5),
('T002', 10, 14),
('T002', 11, 19),
('T002', 12, 20),
('T003', 14, 9),
('T003', 12, 10),
('T003', 7, 6),
('T003', 1, 7),
('T003', 3, 4),
('T004', 1, 1),
('T004', 3, 2),
('T004', 5, 8),
('T005', 4, 1),
('T006', 2, 9),
('T007', 8, 5),
('T008', 2, 6),
('T008', 4, 3),
('T009', 1, 2),
('T009', 5, 5),
('T010', 3, 8);



INSERT INTO DisponibilidadAlmacen VALUES
('T001', 1, 10),
('T001', 2, 20),
('T002', 3, 30),
('T002', 4, 40),
('T003', 5, 50),
('T003', 6, 60),
('T004', 7, 70),
('T004', 8, 80),
('T005', 9, 90),
('T005', 10, 100);



INSERT INTO Compra VALUES 
(DEFAULT),
(DEFAULT),
(DEFAULT),
(DEFAULT),
(DEFAULT),
(DEFAULT),
(DEFAULT),
(DEFAULT),
(DEFAULT),
(DEFAULT);



INSERT INTO Carrito VALUES
(1, 1, 3),
(1, 2, 2),
(2, 2, 1),
(3, 3, 2),
(3, 1, 1),
(4, 5, 3),
(5, 4, 6),
(5, 5, 4),
(5, 10, 10),
(5, 14, 2),
(5, 11, 3),
(6, 8, 10),
(7, 8, 4),
(8, 3, 3),
(9, 14, 2),
(9, 12, 4),
(9, 7, 1),
(10, 1, 1);



INSERT INTO Transaccion VALUES 
(DEFAULT, '12345678A', '87654321A', 'T001', 1),
(DEFAULT, '12345678B', '87654321A', 'T001', 2),
(DEFAULT, '12345678F', '87654321C', 'T003', 3),
(DEFAULT, '12345678D', '87654321D', 'T004', 4),
(DEFAULT, '12345678F', '87654321A', 'T001', 5),
(DEFAULT, '12345678C', '87654321B', 'T002', 6),
(DEFAULT, '12345678G', '87654321A', 'T001', 7),
(DEFAULT, '12345678H', '87654321B', 'T002', 8),
(DEFAULT, '12345678F', '87654321C', 'T003', 9),
(DEFAULT, '12345678D', '87654321D', 'T004', 10);
