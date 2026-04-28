USE dimdim_564928;

SHOW TABLES;

SELECT * FROM transacoes;

-- Depois de fazer INSERT no app.py, rode:
SELECT * FROM transacoes ORDER BY id;

-- Depois de fazer UPDATE no app.py, troque o ID pelo ID atualizado:
SELECT * FROM transacoes WHERE id = 2;

-- Depois de fazer DELETE no app.py, troque o ID pelo ID removido:
SELECT * FROM transacoes WHERE id = 2;
