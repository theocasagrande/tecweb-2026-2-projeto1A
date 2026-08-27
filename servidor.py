import socket
from pathlib import Path
from utils import extract_route, extract_method, read_file, build_response, guess_content_type
from views import (
    index, create_note, confirm_delete, delete_note,
    edit_note_page, save_note_edit, toggle_favorite, not_found,
)


CUR_DIR = Path(__file__).parent

SERVER_HOST = 'localhost'
SERVER_PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

print(f'Servidor escutando em (ctrl+click): http://{SERVER_HOST}:{SERVER_PORT}')

try:
    while True:
        client_connection, client_address = server_socket.accept()

        request = client_connection.recv(1024).decode()
        if not request:
            client_connection.close()
            continue
        print('*'*100)
        print(request)

        method = extract_method(request)
        route = extract_route(request)
        filepath = CUR_DIR / route
        segmentos = route.split('/')
        prefixo = segmentos[0]
        note_id = segmentos[1] if len(segmentos) > 1 else None

        if filepath.is_file():
            headers = f'Content-Type: {guess_content_type(filepath)}'
            response = build_response(headers=headers) + read_file(filepath)
        elif route == '' and method == 'GET':
            response = index(request)
        elif route == '' and method == 'POST':
            response = create_note(request)
        elif prefixo == 'delete' and note_id and method == 'GET':
            response = confirm_delete(note_id)
        elif prefixo == 'delete' and note_id and method == 'POST':
            response = delete_note(note_id)
        elif prefixo == 'edit' and note_id and method == 'GET':
            response = edit_note_page(note_id)
        elif prefixo == 'edit' and note_id and method == 'POST':
            response = save_note_edit(request, note_id)
        elif prefixo == 'favorite' and note_id and method == 'POST':
            response = toggle_favorite(note_id)
        else:
            response = not_found()

        client_connection.sendall(response)

        client_connection.close()
finally:
    server_socket.close()