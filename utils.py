CONTENT_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'text/javascript',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
}
def guess_content_type(path):
    return CONTENT_TYPES.get(path.suffix, 'application/octet-stream')
def extract_route(request):
    separado = request.split()
    route = separado[1]
    return route[1:]
def read_file(path):
    with open(path, 'rb') as f:
        return f.read()
def load_template(filename):
    with open(f'templates/{filename}', 'r', encoding='utf-8') as f:
        return f.read()
def build_response(body='', code=200, reason='OK', headers=''):
    if isinstance(body, str):
        body = body.encode()
    status_line = f'HTTP/1.1 {code} {reason}\n'
    headers_block = f'{headers}\n' if headers else ''
    return (status_line + headers_block + '\n').encode() + body