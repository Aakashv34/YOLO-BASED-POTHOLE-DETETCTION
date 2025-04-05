from django import forms
from .models import DetectionHistory

class DetectionForm(forms.ModelForm):
    class Meta:
        model = DetectionHistory
        fields = ['image']
