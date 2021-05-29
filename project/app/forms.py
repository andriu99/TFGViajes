from django import forms
from datetime import timedelta
from durationwidget.widgets import TimeDurationWidget


class DateInput(forms.DateTimeInput):
    input_type='date'
    
class userRequest(forms.Form):
    def __init__(self, *args, **kwargs):
        super(userRequest,self).__init__(*args, **kwargs)

    lat_Origin = forms.FloatField(widget=forms.HiddenInput(attrs={"id":"lat_Origin"}),required=False,initial=181)
    lon_Origin = forms.FloatField(widget=forms.HiddenInput(attrs={"id":"lon_Origin"}),required=False,initial=181)
    lat_Dest = forms.FloatField(widget=forms.HiddenInput(attrs={"id":"lat_Dest"}),required=False,initial=181)
    lon_Dest = forms.FloatField(widget=forms.HiddenInput(attrs={"id":"lon_Dest"}),required=False,initial=181)

 

    origin_address=forms.CharField(max_length=200,widget=forms.TextInput(attrs={"class":"data","id":"origin_address"}))
    destination_address=forms.CharField(max_length=200,widget=forms.TextInput(attrs={"class":"data","id":"destination_address"}))

    date=forms.DateField(widget=DateInput(attrs={"class":"data"}))

    maxPrice=forms.FloatField(label='Max price:',widget=forms.NumberInput(attrs={"id":"max_price_time","class":"data",'step': "0.1"}),required=False)

    CHOICES =(
    ("NONE", "NONE"),
    ("ASC", "ASC"),
    ("DESC", "DESC"),
    )
    
    OrderType = forms.ChoiceField(label='Order: ',choices = CHOICES,initial='NONE',required=False,widget=forms.Select(attrs={"class":"data","id":"max_price_time"}))


   

