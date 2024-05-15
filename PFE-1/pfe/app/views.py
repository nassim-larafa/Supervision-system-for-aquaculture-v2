from django.shortcuts import render , HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def projets(request):
    return render(request, 'projects.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contacts.html')

def signup(request):
    return render(request, 'signup.html')