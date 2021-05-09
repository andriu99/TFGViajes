from django import forms

class DateInput(forms.DateInput):
    input_type='date'
class userRequest(forms.Form):
    latOrigen = forms.FloatField()
    lonOrigen = forms.FloatField()
    latDest = forms.FloatField()
    lonDest = forms.FloatField()
    date=forms.DateField(widget=DateInput)