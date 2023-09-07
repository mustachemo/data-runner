from django.http import HttpResponse


def index(request):
    return HttpResponse("Error 418 I'm a teapot <a href='https://www.rfc-editor.org/rfc/rfc2324'>RFC2324</a>")