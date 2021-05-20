from django import forms


class DateInput(forms.DateTimeInput):
    input_type='date'
    
class userRequest(forms.Form):
    lat_Origin = forms.FloatField(widget=forms.HiddenInput(attrs={"id":"latO"}),required=False,)
    lon_Origin = forms.FloatField(widget=forms.HiddenInput(attrs={"id":"lonO"}),required=False)
    lat_Dest = forms.FloatField(widget=forms.HiddenInput(attrs={"id":"latD"}),required=False)
    lon_Dest = forms.FloatField(widget=forms.HiddenInput(attrs={"id":"lonD"}),required=False)
    
    def __init__(self, *args, **kwargs):
        super(userRequest,self).__init__(*args, **kwargs)
        
    
    origin_address=forms.CharField(max_length=200,widget=forms.TextInput(attrs={"class":"data","id":"origin_address"}))
    destination_address=forms.CharField(max_length=200,widget=forms.TextInput(attrs={"class":"data","id":"destination_address"}))

    date=forms.DateField(widget=DateInput(attrs={"class":"data"}))