from django.urls import path
from . import views

urlpatterns = [
    path('produtos/', views.produto_list, name='produto_list'),
    path('produtos/novo/', views.produto_create, name='produto_create'),
    path('produtos/<int:pk>/editar/', views.produto_update, name='produto_update'),
    path('produtos/<int:pk>/excluir/', views.produto_delete, name='produto_delete'),

    # Novo endpoint para criar tipo via AJAX
    path('tipos/criar/', views.tipo_produto_create_ajax, name='tipo_produto_create_ajax'),
]
