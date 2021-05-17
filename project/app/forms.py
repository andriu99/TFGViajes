from django import forms

class DateInput(forms.DateTimeInput):
    input_type='date'
    
class userRequest(forms.Form):
    lat_Origin = forms.FloatField(label='Latitude origin')
    lon_Origin = forms.FloatField(label='Longitude origin')
    lat_Dest = forms.FloatField(label='Latitude destination')
    lon_Dest = forms.FloatField(label='Longitude destination')
    date=forms.DateField(widget=DateInput)