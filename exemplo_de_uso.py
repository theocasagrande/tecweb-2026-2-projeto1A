from database import Database, Note

db = Database('banco')

db.add(Note(title='Pão doce', content='Abra o pão e coloque o seu suco em pó favorito.'))
db.add(Note(title=None, content='Lembrar de tomar água'))

notes = db.get_all()
for note in notes:
    print(f'Anotação {note.id}:\n  Título: {note.title}\n  Conteúdo: {note.content}\n')

segunda_nota = notes[1]
segunda_nota.title = 'Lembrete'
db.update(segunda_nota)

print('Após o update:')
for note in db.get_all():
    print(f'Anotação {note.id}:\n  Título: {note.title}\n  Conteúdo: {note.content}\n')

db.delete(notes[0].id)

print('Após o delete:')
for note in db.get_all():
    print(f'Anotação {note.id}:\n  Título: {note.title}\n  Conteúdo: {note.content}\n')
