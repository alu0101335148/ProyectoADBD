-- Consultas que revisan el correcto funcionamiento de los triggers, las restricciones


-- Cambiar el supervisor de la tienda T001.
-- Se espera un error, nunca ha trabajado allí.
UPDATE Almacen
SET ID_SUPER = '12345682E'
WHERE ID_ALM = 'T001';

-- check_cajero: 
INSERT INTO Compra VALUES 
(DEFAULT),
(DEFAULT),
(DEFAULT);

INSERT INTO Carrito VALUES
(4, 1, 3),
(4, 2, 2),
(5, 3, 1),
(6, 4, 2),
(6, 1, 1);

-- no cajero -> error 
INSERT INTO Transaccion VALUES 
(DEFAULT, '12345678A', '12345679B', 'T001', 4),

-- cajero de otra tienda -> error
INSERT INTO Transaccion VALUES
(DEFAULT, '12345678A', '12345679A', 'T002', 5),


-- check producto:
-- producto inexistente en una tienda o con stock insuficiente -> error
INSERT INTO Transaccion VALUES
(DEFAULT, '12345678A', '12345679A', 'T010', 6),