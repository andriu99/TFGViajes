from django import forms

class userRequest(forms.Form):
    latOrigen = forms.FloatField()
    lonOrigen = forms.FloatField()
    latDest = forms.FloatField()
    lonDest = forms.FloatField()