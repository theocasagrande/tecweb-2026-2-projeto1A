def extract_route(request):
    separado = request.split()
    route = separado[1]
    return route[1:]
