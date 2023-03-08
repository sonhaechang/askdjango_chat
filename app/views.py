from django.shortcuts import render

# Create your views here.
def echo_apge(request):
    return render(request, 'app/echo/container/page.html')