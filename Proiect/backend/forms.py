from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from backend.models import Sticker, Cart, CartSticker


class StickerForm(forms.ModelForm):
    class Meta:
        # specify model to be used
        model = Sticker

        # specify fields to be used
        fields = [
            'name', 'length', 'height', 'price', 'image'
        ]

class CustomerForm(UserCreationForm):
    username = forms.CharField(label='username', min_length=5, max_length=150)
    email = forms.EmailField(label='email')
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields[
            'username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields[
            'password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields[
            'password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class CartForm(forms.ModelForm):
    class Meta:
        # specify model to be used
        model = Cart

        # specify fields to be used
        fields = [
            'user', 'stickers'
        ]
    stickers = forms.ModelMultipleChoiceField(
        queryset=Sticker.objects.all(),
        widget=forms.CheckboxSelectMultiple
)

class CartStickerForm(forms.ModelForm):
    class Meta:
        # specify model to be used
        model = CartSticker

        # specify fields to be used
        fields = [
            'cart', 'sticker'
        ]