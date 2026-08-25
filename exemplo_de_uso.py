from database import Database, Note

db = Database('banco')

db.add(Note(title='Pão doce', content='Abra o pão e coloque o seu suco em pó favorito.'))
db.add(Note(title=None, content='Lembrar de tomar água'))
