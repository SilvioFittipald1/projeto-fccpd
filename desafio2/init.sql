CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO usuarios (nome, email) VALUES
    ('João gomes', 'joao@email.com'),
    ('charles oliveira', 'charles@email.com'),
    ('Pedro neto', 'pedro@email.com'),
    ('alex pereira', 'alex@email.com'),
    ('Carlos augusto', 'carlos@email.com');

SELECT 'Banco de dados inicializado com sucesso!' as mensagem;
SELECT COUNT(*) as total_usuarios FROM usuarios;

