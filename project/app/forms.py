from django import forms


class DateInput(forms.DateTimeInput):
    input_type='date'
    
class userRequest(forms.Form):
    def __init__(self, *args, **kwargs):
        super(userRequest,self).__init__(*args, **kwargs)

    lat_Origin = forms.FloatField(widget=forms.HiddenInput(attrs={"id":"lat_Origin"}),required=False,initial=181)
    lon_Origin = forms.FloatField(widget=forms.HiddenInput(attrs={"id":"lon_Origin"}),required=False,initial=181)
    lat_Dest = forms.FloatField(widget=forms.HiddenInput(attrs={"id":"lat_Dest"}),required=False,initial=181)
    lon_Dest = forms.FloatField(widget=forms.HiddenInput(attrs={"id":"lon_Dest"}),required=False,initial=181)

    lat_currentLocat= forms.FloatField(widget=forms.HiddenInput(attrs={"id":"lat_currentLocat"}),required=False,initial=181) 
    lon_currentLocat= forms.FloatField(widget=forms.HiddenInput(attrs={"id":"lon_currentLocat"}),required=False,initial=181)


    current_address=forms.CharField(max_length=200,widget=forms.HiddenInput(attrs={"class":"data","id":"current_address"}),initial='.')
    origin_address=forms.CharField(max_length=200,widget=forms.TextInput(attrs={"class":"data","id":"origin_address"}))
    destination_address=forms.CharField(max_length=200,widget=forms.TextInput(attrs={"class":"data","id":"destination_address"}))

    date=forms.DateField(widget=DateInput(attrs={"class":"data"}))