import json

def extract_route(request):
    separado = request.split()
    route = separado[1]
    return route[1:]
def read_file(path):
    with open(path, 'rb') as f:
        return f.read()
def load_data(filename):
    with open(f'data/{filename}', 'r', encoding='utf-8') as f:
        return json.load(f)
def load_template(filename):
    with open(f'templates/{filename}', 'r', encoding='utf-8') as f:
        return f.read()
def save_note(titulo, detalhes):
    notes = load_data('notes.json')
    notes.append({'titulo': titulo, 'detalhes': detalhes})
    with open('data/notes.json', 'w', encoding='utf-8') as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)
def build_response(body='', code=200, reason='OK', headers=''):
    if isinstance(body, str):
        body = body.encode()
    status_line = f'HTTP/1.1 {code} {reason}\n'
    headers_block = f'{headers}\n' if headers else ''
    return (status_line + headers_block + '\n').encode() + body