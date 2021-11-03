from django import forms


class LoginForm(forms.Form):
    access_code = forms.CharField(
        label="access_code",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 placeholder-gray-300 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-indigo-100 focus:border-indigo-300",
                "placeholder": "Your access code",
            }
        ),
    )
