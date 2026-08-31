from urllib.parse import unquote_plus

CONTENT_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
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
def extract_method(request):
    return request.split()[0]
def extract_body(request):
    partes = request.replace('\r', '').split('\n\n', 1)
    return partes[1] if len(partes) > 1 else ''
def content_length(request):
    for linha in request.replace('\r', '').split('\n'):
        if linha.lower().startswith('content-length:'):
            return int(linha.split(':', 1)[1])
    return 0
def read_request(connection):
    request = connection.recv(1024).decode()
    if not request:
        return request

    tamanho = content_length(request)
    while len(extract_body(request)) < tamanho:
        request += connection.recv(1024).decode()
    return request
def parse_post_params(request):
    params = {}
    for chave_valor in extract_body(request).split('&'):
        chave, valor = chave_valor.split('=')
        params[chave] = unquote_plus(valor)
    return params
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