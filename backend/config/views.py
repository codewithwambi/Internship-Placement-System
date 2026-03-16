from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>  hello team Internship System Backend is Running  smoothly!</h1><p>Go to <a href='/admin/'>/admin/</a> to manage placements.</p>")