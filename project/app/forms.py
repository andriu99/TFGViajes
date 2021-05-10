from django import forms

class DateInput(forms.DateInput):
    input_type='date'
    
class userRequest(forms.Form):
    lat_Origin = forms.FloatField(label='Latitude origin')
    lon_Origin = forms.FloatField(label='Longitude destination')
    lat_Dest = forms.FloatField(label='Latitude origin')
    lon_Dest = forms.FloatField(label='Longitude destination')
    date=forms.DateField(widget=DateInput)