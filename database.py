import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='admin'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `cursos`;")

cursor.execute("CREATE DATABASE `cursos`;")

cursor.execute("USE `cursos`;")

TABLES = {}
TABLES['Cursos'] = ('''
      CREATE TABLE `cursos` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `duracao` varchar(40) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['adm'] = ('''
      CREATE TABLE `adm` (
      `nome` varchar(20) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nome`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print('Criando tabela {}:'.format(tabela_nome), end=' ')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Já existe')
        else:
            print(err.msg)
    else:
        print('OK')


# inserindo usuarios
adm_sql = 'INSERT INTO adm (nome, senha) VALUES (%s, %s)'
usuarios = [
    ("admin", "@admin1234"),
]
cursor.executemany(adm_sql, usuarios)

cursor.execute('select * from cursos.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
cursos_sql = 'INSERT INTO cursos (nome, duracao) VALUES (%s, %s)'
cursos = [
    ('HTML+CSS', '20h'),
    ('JavaScript Completo', '40h'),
    ('React', '16h'),
    ('Python', '40h'),
    ('AWS', '16h'),
]
cursor.executemany(cursos_sql, cursos)

cursor.execute('select * from cursos.cursos')
print(' -------------  Cursos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando se não nada tem efeito
conn.commit()
cursor.close()
conn.close()
