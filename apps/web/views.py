from django.shortcuts import render

# Create your views here.

def home(request): return render(request, "templates/home.html")
def practice(request): return render(request, "templates/text/practice.html")
def voice_live(request): return render(request, "templates/voice/live.html")