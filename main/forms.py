from django import forms
from .models import HopDong

class HopDongForm(forms.ModelForm):
    class Meta:
        model = HopDong
        fields = '__all__'