import random
from utils import load_template, build_response, parse_post_params
from database import Database, Note

db = Database('banco')

REDIRECT_HOME = build_response(code=303, reason='See Other', headers='Location: /')

ERROR_TEMPLATE = '<p class="form-error">{erro}</p>'

def random_card_classes():
    cor = random.randint(1, 5)
    rotacao = random.randint(1, 11)
    return f'card-color-{cor} card-rotation-{rotacao}'

def render_notes():
    # Cria uma lista de cards para cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    note_template = load_template('components/note.html')
    cards = [
        note_template.format(
            id=nota.id,
            title=nota.title,
            details=nota.content,
            favorite_icon='★' if nota.favorite else '☆',
            classes=random_card_classes(),
        )
        for nota in db.get_all()
    ]
    return '\n'.join(cards)

def index(request, erro=''):
    mensagem = ERROR_TEMPLATE.format(erro=erro) if erro else ''
    body = load_template('index.html').format(notes=render_notes(), erro=mensagem)
    return build_response(body=body)

def create_note(request):
    params = parse_post_params(request)
    titulo = params['titulo'].strip()
    detalhes = params['detalhes'].strip()
    if not titulo or not detalhes:
        return index(request, erro='Preencha o título e o conteúdo para criar uma anotação.')

    db.add(Note(title=titulo, content=detalhes))
    return REDIRECT_HOME

def confirm_delete(note_id):
    nota = db.get_by_id(int(note_id))
    if nota is None:
        return not_found()

    body = load_template('confirm_delete.html').format(
        id=nota.id, title=nota.title, details=nota.content, classes=random_card_classes()
    )
    return build_response(body=body)

def delete_note(note_id):
    db.delete(int(note_id))
    return REDIRECT_HOME

def edit_note_page(note_id, title=None, details=None, erro=''):
    nota = db.get_by_id(int(note_id))
    if nota is None:
        return not_found()

    mensagem = ERROR_TEMPLATE.format(erro=erro) if erro else ''
    body = load_template('edit.html').format(
        id=nota.id,
        title=nota.title if title is None else title,
        details=nota.content if details is None else details,
        erro=mensagem,
    )
    return build_response(body=body)

def save_note_edit(request, note_id):
    params = parse_post_params(request)
    titulo = params['titulo'].strip()
    detalhes = params['detalhes'].strip()
    if not titulo or not detalhes:
        return edit_note_page(
            note_id, title=titulo, details=detalhes,
            erro='Preencha o título e o conteúdo para salvar a anotação.',
        )

    db.update(Note(id=int(note_id), title=titulo, content=detalhes))
    return REDIRECT_HOME

def toggle_favorite(note_id):
    db.toggle_favorite(int(note_id))
    return REDIRECT_HOME

def not_found():
    body = load_template('404.html')
    return build_response(code=404, reason='Not Found', body=body)