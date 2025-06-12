from django import forms
from .models import UserPayment


class TransactionInfoForm(forms.ModelForm):
    value = forms.CharField(max_length=50, required=False)
    email = forms.EmailField()

    class Meta:
        model = UserPayment
        fields = ("value", "email")
