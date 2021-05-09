from django.shortcuts import render
from .forms import userRequest
from app.models import Request,RESTApi,Node
import datetime

def home(request):
    if request.method == 'POST':
        form = userRequest(request.POST)
        if form.is_valid():
            getBlablaCarTrips=Request.objects.get(name='getBlablaCarTrips')
            print(type(form.cleaned_data['date']))
            end_date_local=form.cleaned_data['date']+datetime.timedelta(days=1)
            
            #getBlablaCarTrips.execute([getBlablaCarTrips.RApi.APIKey,,,'EUR',form.cleaned_data['date'].isoformat(),form.])
            print(form.cleaned_data['date'].isoformat())
       
    else:
        form = userRequest()
    

    context = {'form' : form}
    return render(request,'app/home.html',context)