from django import forms

class DateInput(forms.DateInput):
    input_type='date'
    
class userRequest(forms.Form):
    lat_Origin = forms.FloatField()
    lon_Origin = forms.FloatField()
    lat_Dest = forms.FloatField()
    lon_Dest = forms.FloatField()
    date=forms.DateField(widget=DateInput)