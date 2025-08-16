from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from estoque.views import CustomLoginView, primeiro_login_view  # <<< importa nossas novas views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Autenticação
    path('login/', CustomLoginView.as_view(), name='login'),   # <<< substitui o LoginView padrão
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('primeiro-login/', primeiro_login_view, name='primeiro_login'),  # <<< novo endpoint

    # App estoque
    path('', include('estoque.urls')),
]
