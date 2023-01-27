from django import forms


class LoginForm(forms.Form):
    access_code = forms.CharField(
        label="access_code",
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-3 py-2 placeholder-gray-300 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-indigo-100 focus:border-indigo-300",
                "placeholder": "Your access code",
            }
        ),
    )


class ConfigForm(forms.Form):
    flip_order_by_name = forms.BooleanField(
        label="Flip order by name",
        required=False,
        initial=True,
    )

    show_num_assignments = forms.BooleanField(
        label="Show number of assignments",
        required=False,
        initial=True,
    )

    show_solfege = forms.BooleanField(
        label="Show solfege",
        required=False,
        initial=True,
    )
