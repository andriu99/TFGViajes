from django import forms
from places.fields import PlacesField
from location_field.forms.plain import PlainLocationField


class DateInput(forms.DateTimeInput):
    input_type='date'
    
class userRequest(forms.Form):
    lat_Origin = forms.FloatField(widget=forms.HiddenInput())
    lon_Origin = forms.FloatField(widget=forms.HiddenInput())
    lat_Dest = forms.FloatField(widget=forms.HiddenInput())
    lon_Dest = forms.FloatField(widget=forms.HiddenInput())
    
    def __init__(self, *args, **kwargs):
        super(userRequest,self).__init__(*args, **kwargs)
        
    
    origin_address=forms.CharField(max_length=200,widget=forms.TextInput(attrs={"class":"data","id":"origin_address"}))
    destination_address=forms.CharField(max_length=200,widget=forms.TextInput(attrs={"class":"data","id":"destination_address"}))

    date=forms.DateField(widget=DateInput(attrs={"class":"data"}))