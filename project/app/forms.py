from django import forms


class DateInput(forms.DateTimeInput):
    input_type='date'
    
class userRequest(forms.Form):
    def __init__(self, *args, **kwargs):
        super(userRequest, self).__init__(*args, **kwargs)


    lat_Origin = forms.FloatField(widget=forms.HiddenInput(attrs={'id':'lat_Origin'}),required=False,initial=181)
    lon_Origin = forms.FloatField(widget=forms.HiddenInput(attrs={'id':'lon_Origin'}),required=False,initial=181)
    lat_Dest = forms.FloatField(widget=forms.HiddenInput(attrs={'id':'lat_Dest'}),required=False,initial=181)
    lon_Dest = forms.FloatField(widget=forms.HiddenInput(attrs={'id':'lon_Dest'}),required=False,initial=181)

    origin_address=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'data_aux data','id':'origin_address'}))
    destination_address=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'data_aux data','id':'destination_address'}))


    date=forms.DateField(widget=DateInput(attrs={'class':'data_aux data','id':'data_id'}))

    maxPrice=forms.FloatField(label='Max price:',widget=forms.NumberInput(attrs={'class':'data_aux data order','step': '0.1'}),required=False)

    CHOICES_ORDERTYPE =(
    ('NONE', 'NONE'),
    ('ASC', 'ASC'),
    ('DESC', 'DESC'),
    )
    
    OrderType = forms.ChoiceField(label='Order',choices = CHOICES_ORDERTYPE,initial='NONE',required=False,widget=forms.Select(attrs={'class':'data order'}))

    CHOICES_ORDERBY =(
    ('PRICE', 'PRICE'),
    ('DURATION', 'DURATION'),
    )
    OrderBy = forms.ChoiceField(label='Order by',choices = CHOICES_ORDERBY,initial='PRICE',required=False,widget=forms.Select(attrs={'class':'data order'}))





