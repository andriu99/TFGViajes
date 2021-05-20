from django import forms
from places.fields import PlacesField
from location_field.forms.plain import PlainLocationField


class DateInput(forms.DateTimeInput):
    input_type='date'
    
class userRequest(forms.Form):
    # lat_Origin = forms.FloatField(label='Latitude origin')
    # lon_Origin = forms.FloatField(label='Longitude origin')
    # lat_Dest = forms.FloatField(label='Latitude destination')
    # lon_Dest = forms.FloatField(label='Longitude destination')
    
    def __init__(self, *args, **kwargs):
        super(userRequest,self).__init__(*args, **kwargs)
        
    #a=forms.CharField(choices=[],required=True)
    
    origin_address=forms.CharField(max_length=200,widget=forms.TextInput(attrs={"class":"data","id":"origin_address"}))
    destination_address=forms.CharField(max_length=200,widget=forms.TextInput(attrs={"class":"data","id":"destination_address"}))

    #destination_address=forms.CharField(label='Dirección de llegada')
    date=forms.DateField(widget=DateInput(attrs={"class":"data"}))