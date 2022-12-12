-- Active: 1670869174493@@127.0.0.1@3306@projeto_canela
CREATE DATABASE IF NOT EXISTS projeto_canela
    DEFAULT CHARACTER SET = 'utf8mb4';

CREATE TABLE IF NOT EXISTS VENDAS(  
    id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    nome VARCHAR(255),
    preco FLOAT,
    descricao VARCHAR(255),
    quantidade INT
) COMMENT '';


INSERT INTO VENDAS (nome, preco, descricao, quantidade) 
VALUES
("maçã", 5.78, "maçã tamanho médio", 15),
("mesa", 265.00, "mesa cor cinza", 2),
("relógio", 20.50, "relógio de pulso preto com branco", 3),
("garrafa", 65.78, "garrafa térmica de aço inoxidável", 8),
("mouse", 25, "mouse da marca logitech", 4),
("monitor", 700, "monitor full hd 24 polegadas", 3),
("pêra", 5.78, "pêra tamanho médio", 15),
("cadeira", 100.00, "cadeira cor laranja", 2),
("abacaxi", 20.50, "abacaxi tamanho grande", 13),
("canela", 10.78, "canela térmica de aço inoxidável", 8),
("alface", 5, "alface lisa", 8),
("cereja", 20.00, "Bandeja de cereja 250g", 16),
("tomate", 10.53, "Tomate em lata", 5),
("pepino", 7.98, "pepino 1/kg", 9),
("couve", 8.50, "couve galega", 7);


SELECT * from `VENDAS`;

-- SELECT * FROM VENDAS ORDER BY quantidade DESC;
 
-- DELETE FROM VENDAS;

-- SELECT COUNT(nome) as total_produtos, SUM(quantidade) as total_quantidade, ROUND(SUM(preco), 2) as total_preco from VENDAS;

