CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO usuarios (nome, email) VALUES
    ('Renato Moicano', 'renato@email.com'),
    ('Edson Barboza', 'edson@email.com'),
    ('Diego Lopes', 'diego@email.com'),
    ('Alexandre Pantoja', 'alexandre@email.com'),
    ('Valter Walker', 'valter@email.com')
ON CONFLICT (email) DO NOTHING;

SELECT 'Banco de dados desafio3_db inicializado com sucesso!' as mensagem;

