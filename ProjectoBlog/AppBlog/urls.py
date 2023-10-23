from django.urls import path
from django.contrib.auth.views import LogoutView
from AppBlog import views
from .views import PostCreacion

urlpatterns = [
    path('', views.inicio, name="Inicio"),
    path('postlist/', views.PostList.as_view(), name="Postlist"),
    path('login/', views.login_request, name="Login"),
    path('register/', views.register, name="Register"),
    path('edit/', views.edit, name="Edit"),
    path('logout/', LogoutView.as_view(template_name = "AppBlog/logout.html"), name="Logout"),
    path('about/', views.about, name="About"),
    path('postcreacion/', PostCreacion.as_view(), name='New'),
    path('postdetail/<int:pk>/', views.PostDetail.as_view(), name="PostDetail"),
    path('postedit/<int:pk>/', views.PostEdit.as_view(), name="PostEdit"),
    path('postdelete/<int:pk>/', views.PostDelete.as_view(), name="PostDelete"),
]
