from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                             'id': 'form2Example1',
                                                                             'type': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'form2Example2',
        'type': 'password',
    }))


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                             'id': 'username_field',
                                                                             'type': 'username'}))
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'id': 'email_field',
                                                                           'type': 'email'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                               'id': 'firstname_field'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                              'id': 'lastname_field',
                                                                              }))
    password_1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password1_field',
        'type': 'password',
    }))

    password_2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password2_field',
        'type': 'password',
    }))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password_1 = cleaned_data.get('password_1')
        password_2 = cleaned_data.get('password_2')

        if password_1 != password_2:
            self.add_error('password_2', 'رمز های وارد شده یکسان نیستند')

        if len(password_1) < 8:
            self.add_error('password_1', 'رمز وارد شده کوچک است. رمز باید بیشتر از 8 رقم داشته باشد')

        if User.objects.filter(username=username):
            self.add_error('username', 'نام کاربری وارد شده وجود دارد. لطفا یک نام کاربری دیگر وارد کنید')

        if User.objects.filter(email=email):
            self.add_error('email', 'ایمیل وارد شده وجود دارد. لطفا یک ایمیل دیگر وارد کنید')

        return cleaned_data
