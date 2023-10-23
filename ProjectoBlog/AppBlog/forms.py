from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from AppBlog.models import Posts

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label="Contraseña" , widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir Contraseña" , widget=forms.PasswordInput)
    username = forms.CharField(
        label="Username",
        help_text=None
    )
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        helps_texts = {k:"" for k in fields}
        

class UserEditForm(UserCreationForm):

    email = forms.EmailField(label="Ingrese su email:")
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir la contraseña', widget=forms.PasswordInput)

    last_name = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    imagen = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['email', 'last_name', 'first_name', 'password1', 'password2']

class PostFormulario(forms.Form):
    titulo = forms.TextInput()
    descripcion = forms.Textarea()
    email = forms.EmailField()
    imagenPost = forms.ImageField(required=False)

class PostUpdate(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ["titulo", "descripcion", "email", "imagenPost"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['imagenPost'].required = False