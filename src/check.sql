-- Consultas que revisan el correcto funcionamiento de los triggers, las restricciones


-- Cambiar el supervisor de la tienda T001.
-- Se espera un error, el empleado nunca ha trabajado allí.
UPDATE Almacen
SET DNI_SUPER = '87654321J'
WHERE ID_ALM = 'T001';

-- check_cajero: 
INSERT INTO Compra VALUES 
(5000),
(5001),
(5002);

INSERT INTO Carrito VALUES
(5000, 1, 3),
(5000, 2, 2),
(5001, 3, 1),
(5002, 4, 2),
(5002, 1, 1000);

-- trabaja en T001, pero no es cajero -> error 
INSERT INTO Transaccion VALUES 
(DEFAULT, '12345678A', '87654321E', 'T001', 5000);

-- cajero de otra tienda -> error
INSERT INTO Transaccion VALUES
(DEFAULT, '12345678A', '87654321A', 'T002', 5001);


-- check producto:
-- producto inexistente en una tienda o con stock insuficiente -> error
INSERT INTO Transaccion VALUES
(DEFAULT, '12345678A', '87654321A', 'T001', 5002);