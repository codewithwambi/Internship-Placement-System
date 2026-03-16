from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Internship System Backend is Running!</h1><p>Go to <a href='/admin/'>/admin/</a> to manage placements.</p>")