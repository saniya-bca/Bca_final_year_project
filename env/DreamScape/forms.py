import re
from django import forms
from django.contrib.auth.models import User
from .models import ContactMessage

class UpiPaymentForm(forms.Form):
    upi_id = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your UPI ID'})
    )

    def clean_upi_id(self):
        upi_id = self.cleaned_data.get('upi_id')
        upi_regex = r'^[\w.-]+@[\w.-]+$'
        if not re.match(upi_regex, upi_id):
            raise forms.ValidationError("Enter a valid UPI ID.")
        return upi_id

class CardPaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16, label="Card Number")
    expiry_date = forms.CharField(max_length=5, label="Expiry Date (MM/YY)")
    cvv = forms.CharField(max_length=3, label="CVV")

class NetbankingPaymentForm(forms.Form):
    account_number = forms.CharField(max_length=20, label="Account Number")
    ifsc_code = forms.CharField(max_length=11, label="IFSC Code")

class PaytmPaymentForm(forms.Form):
    paytm_number = forms.CharField(max_length=10, label="Paytm Mobile Number")

    
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']