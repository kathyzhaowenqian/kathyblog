from django.shortcuts import render
from django.views import View
from django.http import JsonResponse,HttpResponse

from django.shortcuts import redirect

# Create your views here.
class MainPage(View):
    def get(self,request):
        return render(request, 'index.html')
    
class ABOUT(View):
    def get(self,request):
        return render(request, 'about.html')

class PROJECT(View):
    def get(self,request):
        return render(request, 'project.html')
    
class GALLERY(View):
    def get(self,request):
        return render(request, 'gallery.html')

class KNOWLEDGE(View):
    def get(self,request):
        return render(request, 'knowledge.html')

class CONTACT(View):
    def get(self,request):
        return render(request, 'contact.html')  

    
class DRAGON_GAME(View):
    def get(self,request):
        return redirect('http://127.0.0.1:8501')