from django.shortcuts import render

def home(request):
    
    if request.method == 'POST':
        form = userRequest(request.POST)

        if form.is_valid():
		    tarea = form.cleaned_data["tarea"]
    else:
        form = userRequest()


    return render(request,'app/home.html')