-- Active: 1666902268649@@127.0.0.1@3306@projeto_canela
CREATE DATABASE IF NOT EXISTS projeto_canela
    DEFAULT CHARACTER SET = 'utf8mb4';

CREATE TABLE IF NOT EXISTS VENDAS(  
    id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    nome VARCHAR(255),
    preco FLOAT,
    quantidade INT
) COMMENT '';


INSERT INTO VENDAS (nome, preco, quantidade) 
VALUES
("maçã", 5.78, 15),
("mesa", 265.00, 2),
("relógio", 20.50, 3),
("garrafa", 65.78, 8),
("mouse", 25,4),
("monitor", 700, 3),
("pêra", 5.78,  15),
("cadeira", 100.00,2),
("abacaxi", 20.50, 13),
("canela", 10.78, 8),
("alface", 5, 8),
("cereja", 20.00,16),
("tomate", 10.53, 5),
("pepino", 7.98, 9),
("couve", 8.50, 7);


SELECT * from `VENDAS`;

-- SELECT * FROM VENDAS ORDER BY quantidade DESC;
 
DELETE FROM VENDAS;

-- SELECT COUNT(nome) as total_produtos, SUM(quantidade) as total_quantidade, ROUND(SUM(preco), 2) as total_preco from VENDAS;

