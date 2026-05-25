-- CRIAÇÃO DO BANCO
CREATE TABLE usuarios (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT NOT NULL,

    email TEXT UNIQUE NOT NULL,

    senha TEXT NOT NULL,

    tipo TEXT NOT NULL,

    foto TEXT DEFAULT 'default.png'
);

CREATE TABLE cursos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT NOT NULL,

    descricao TEXT NOT NULL,

    carga_horaria INTEGER NOT NULL,

    duracao TEXT NOT NULL,

    vagas INTEGER NOT NULL
);

INSERT INTO cursos
(
    nome,
    descricao,
    carga_horaria,
    duracao,
    vagas
)

VALUES

(
    'Desenvolvimento de Sistemas',
    'Curso voltado para programação web.',
    1200,
    '18 meses',
    40
),

(
    'Automação Industrial',
    'Curso de automação e controle.',
    1000,
    '16 meses',
    30
);
VALUES

(
'Desenvolvimento de Sistemas',
'Curso voltado para programação web, banco de dados e software.',
1200,
'18 meses',
40
),

(
'Automação Industrial',
'Automação, sensores e controle industrial.',
1000,
'16 meses',
30
),

(
'Mecatrônica',
'Integração de sistemas mecânicos e eletrônicos.',
1400,
'24 meses',
25
);