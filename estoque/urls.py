from django.urls import path
from . import views

urlpatterns = [

    # Página inicial agora vai direto para a página de listagem de produtos
    path('', views.produto_list, name='home'),

    path('fornecedores/', views.produto_list, name='produto_list'),

    path('produtos/', views.produto_list, name='produto_list'),
    path('produtos/novo/', views.produto_create, name='produto_create'),
    path('produtos/<int:pk>/editar/', views.produto_update, name='produto_update'),
    path('produtos/<int:pk>/excluir/', views.produto_delete, name='produto_delete'),

    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/novo/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/editar/', views.cliente_update, name='cliente_update'),
    path('clientes/<int:pk>/excluir/', views.cliente_delete, name='cliente_delete'),

    path('clientes/<int:pk>/contatos/', views.cliente_contatos_ajax, name='cliente_contatos_ajax'),

    # Novo endpoint para criar tipo via AJAX
    path('tipos/criar/', views.tipo_produto_create_ajax, name='tipo_produto_create_ajax'),
    path('unidades/criar/', views.unidade_create_ajax, name='unidade_create_ajax'),
]
