from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from AppBlog.forms import UserRegisterForm, UserEditForm
from django.contrib.auth.decorators import login_required
from AppBlog.models import Avatar, Posts
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy 
from AppBlog.forms import PostUpdate
import pdb

# Create your views here.

def inicio(request):
    return render(request, "AppBlog/index.html")


def about(request):
    return render(request, "AppBlog/about.html")

def login_request(request):
    msg_login = ""
    if request.method =="POST":
        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():
            usuario = form.cleaned_data.get("username")
            clave = form.cleaned_data.get("password")

            nombre_usuario = authenticate(username=usuario, password=clave)

            if usuario is not None:
                login(request, nombre_usuario)
                return render(request, "AppBlog/postlist.html")
        
        msg_login = "Usuario o contraseña incorrectos"
    
    form = AuthenticationForm()
    return render(request, "AppBlog/login.html", {"form": form, "msg_login": msg_login})

def register(request):
    msg_register = ""
    if request.method == "POST":

        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "AppBlog/index.html")
        
        msg_register = "Error en los datos ingresados"
    
    form = UserRegisterForm()
    return render(request, "AppBlog/register.html", {"form":form, "msg_register": msg_register})

@login_required
def edit(request):

    usuario = request.user

    if request.method == 'POST':

        miFormulario = UserEditForm(request.POST)

        if miFormulario.is_valid():

            informacion = miFormulario.cleaned_data

            if informacion["password1"] != informacion["password2"]:
                datos = {
                "last_name": usuario.last_name,
                "first_name": usuario.first_name,
                'email': usuario.email
                }
                miFormulario = UserEditForm(initial=datos)

            else:
                usuario.email = informacion['email']
                if informacion['password1']:
                    usuario.set_password(informacion["password1"])
                usuario.last_name = informacion['last_name']
                usuario.first_name = informacion['first_name']

                usuario.save()

                try:
                    avatar = Avatar.objects.get(user=usuario)
                except Avatar.DoesNotExist:
                    avatar = Avatar(user=usuario, imagen=informacion["imagen"])
                    avatar.save()
                else:
                    avatar.imagen = informacion["imagen"]
                    avatar.save()

                return render(request, "AppBlog/index.html")

    
    else:
        datos = {
            "last_name": usuario.last_name,
            "first_name": usuario.first_name,
            'email': usuario.email
         }
        miFormulario = UserEditForm(initial=datos)

    return render(request, "AppBlog/edit.html", {"mi_form": miFormulario, "usuario": usuario})


class PostCreacion(LoginRequiredMixin, CreateView):
    model = Posts
    template_name = 'AppBlog/postCreacion.html'
    fields = ["titulo", "descripcion", "email", "imagenPost"]
    success_url = reverse_lazy('Postlist')

    def form_valid(self, form):
        # Asigna el usuario actual como el autor del post antes de guardarlo
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class PostList(LoginRequiredMixin, ListView):
    model = Posts
    template_name = "AppBlog/postlist.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

   
class PostDetail(LoginRequiredMixin, DetailView):
    model = Posts
    template_name = "AppBlog/postdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.object.usuario  # Obtén el autor del post

        if author is not None:
            context['author_name'] = author.username  # Nombre del autor del post
        else:
            context['author_name'] = "Usuario Desconocido"  # Opcional: Define un mensaje para usuarios sin nombre

        return context


class PostEdit(LoginRequiredMixin, UpdateView):
    model = Posts
    form_class = PostUpdate
    template_name = "AppBlog/postedit.html"
    success_url = reverse_lazy("Postlist")

    
    

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Posts
    success_url = reverse_lazy("Postlist")
    template_name = 'AppBlog/postdelete.html'
