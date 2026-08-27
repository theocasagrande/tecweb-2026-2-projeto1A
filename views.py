from urllib.parse import unquote_plus
from utils import load_template, build_response
from database import Database, Note

db = Database('banco')

def index(request):
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    if request.startswith('POST'):
        request = request.replace('\r', '')
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=')
            params[chave] = unquote_plus(valor)

        db.add(Note(title=params['titulo'], content=params['detalhes']))

        return build_response(code=303, reason='See Other', headers='Location: /')

    # Cria uma lista de cards para cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(title=nota.title, details=nota.content)
        for nota in db.get_all()
    ]
    notes = '\n'.join(notes_li)

    body = load_template('index.html').format(notes=notes)
    return build_response(body=body)