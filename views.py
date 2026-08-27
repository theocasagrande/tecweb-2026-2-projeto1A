from utils import load_template, build_response, parse_post_params
from database import Database, Note

db = Database('banco')

REDIRECT_HOME = build_response(code=303, reason='See Other', headers='Location: /')

def render_notes():
    # Cria uma lista de cards para cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    note_template = load_template('components/note.html')
    cards = [
        note_template.format(id=nota.id, title=nota.title, details=nota.content)
        for nota in db.get_all()
    ]
    return '\n'.join(cards)

def index(request):
    body = load_template('index.html').format(notes=render_notes())
    return build_response(body=body)

def create_note(request):
    params = parse_post_params(request)
    db.add(Note(title=params['titulo'], content=params['detalhes']))
    return REDIRECT_HOME

def confirm_delete(note_id):
    nota = db.get_by_id(int(note_id))
    body = load_template('confirm_delete.html').format(
        id=nota.id, title=nota.title, details=nota.content
    )
    return build_response(body=body)

def delete_note(note_id):
    db.delete(int(note_id))
    return REDIRECT_HOME