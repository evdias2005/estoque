from django.shortcuts import render

def cadastro_view(request):
    return render(request, 'cadastro.html')

def movimentacao_view(request):
    return render(request, 'movimentacao.html')

def relatorios_view(request):
    return render(request, 'relatorios.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Produto, Cliente
from .forms import ProdutoForm, ClienteForm



from django.http import JsonResponse
from .models import Produto, TipoProduto, Unidade, Cliente
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.core.paginator import Paginator

#------------------------------------------------------------------------------------------------------------------------

# Views relacionadas aos Produtos
# Listagem
@login_required(login_url='login')
def produto_list(request):
    query = request.GET.get('q')
    produtos = Produto.objects.select_related('tipo_produto').order_by('descricao')
    if query:
        produtos = produtos.filter(descricao__icontains=query)

    paginator = Paginator(produtos, 10)  # 10 produtos por página
    page_number = request.GET.get('page')
    produtos = paginator.get_page(page_number)

    return render(request, 'produto_list.html', {'produtos': produtos})


# Criar
@login_required
def produto_create(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Novo produto cadastrado com sucesso!')
            return redirect('produto_list')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = ProdutoForm()
    return render(request, 'produto_form.html', {'form': form, 'acao': 'Novo'})


# Editar
@login_required
def produto_update(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Produto {produto.descricao} foi atualizado com sucesso!')
            return redirect('produto_list')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produto_form.html', {'form': form, 'acao': 'Editar'})


# Excluir
@login_required
def produto_delete(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, f'Produto {produto.descricao} foi excluído com sucesso!')
        return redirect('produto_list')
    return render(request, 'produto_confirm_delete.html', {'produto': produto})


# Funções para cadastrar tipo via AJAX
@csrf_exempt
@require_POST
@login_required
def tipo_produto_create_ajax(request):
    nome = request.POST.get("nome", "").strip()
    if not nome:
        return JsonResponse({"error": "O nome do tipo é obrigatório."}, status=400)

    tipo, created = TipoProduto.objects.get_or_create(nome=nome)
    if not created:
        return JsonResponse({"error": "Já existe um tipo com esse nome."}, status=400)

    return JsonResponse({"id": tipo.id, "nome": tipo.nome})


@csrf_exempt
@require_POST
@login_required
def unidade_create_ajax(request):
    nome = request.POST.get("nome", "").strip()
    if not nome:
        return JsonResponse({"error": "O nome da unidade é obrigatório."}, status=400)

    unidade, created = Unidade.objects.get_or_create(nome=nome)
    if not created:
        return JsonResponse({"error": "Já existe uma unidade com esse nome."}, status=400)

    return JsonResponse({"id": unidade.id, "nome": unidade.nome})

#------------------------------------------------------------------------------------------------------------------------

# Views relacionadas aos Clientes
# Listagem
@login_required(login_url='login')
def cliente_list(request):
    query = request.GET.get('q')
    clientes = Cliente.objects.order_by('nome')
    if query:
        clientes = clientes.filter(nome__icontains=query)

    paginator = Paginator(clientes, 10)  # 10 produtos por página
    page_number = request.GET.get('page')
    clientes = paginator.get_page(page_number)

    return render(request, 'cliente_list.html', {'clientes': clientes})


# Criar
@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Novo cliente cadastrado com sucesso!')
            return redirect('cliente_list')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = ClienteForm()
    return render(request, 'cliente_form.html', {'form': form, 'acao': 'Novo'})


# Editar
@login_required
def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cliente {cliente.nome} foi atualizado com sucesso!')
            return redirect('cliente_list')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'cliente_form.html', {'form': form, 'acao': 'Editar'})


# Excluir
@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, f'Cliente {cliente.nome} foi excluído com sucesso!')
        return redirect('cliente_list')
    return render(request, 'cliente_confirm_delete.html', {'cliente': cliente})

