from django.shortcuts import render
from .forms import userRequest


def home(request):
    if request.method == 'POST':
        form = userRequest(request.POST)
        if form.is_valid():
           print(form.cleaned_data)
       
    else:
        form = userRequest()
    

    context = {'form' : form}
    return render(request,'app/home.html',context)