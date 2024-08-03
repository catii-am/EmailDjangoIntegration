from django import forms
from .models import EmailAccount


class EmailAccountForm(forms.ModelForm):
    class Meta:
        model = EmailAccount
        fields = ['email', 'password', 'provider']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if EmailAccount.objects.filter(email=email).exists():
            raise forms.ValidationError("Email account with this Email already exists.")
        return email
