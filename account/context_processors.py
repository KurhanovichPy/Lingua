def username(request):
    user = str(request.user)
    return {'username': user}
