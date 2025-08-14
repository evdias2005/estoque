from django.shortcuts import render

def cadastro_view(request):
    return render(request, 'cadastro.html')

def movimentacao_view(request):
    return render(request, 'movimentacao.html')

def relatorios_view(request):
    return render(request, 'relatorios.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Produto, TipoProduto, Unidade, Cliente, Contato
from .forms import ProdutoForm, ClienteForm, ContatoFormSet

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.core.paginator import Paginator
from django.http import JsonResponse

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
        produto.is_excluido = True
        produto.save()
        # produto.delete()
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


# Criar cliente
@login_required
def cliente_create(request):
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST)
        contato_formset = ContatoFormSet(request.POST)
        if cliente_form.is_valid() and contato_formset.is_valid():
            cliente = cliente_form.save()
            contato_formset.instance = cliente
            contato_formset.save()
            messages.success(request, 'Novo cliente e contatos cadastrados com sucesso!')
            return redirect('cliente_list')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        cliente_form = ClienteForm()
        contato_formset = ContatoFormSet()
    return render(request, 'cliente_form.html', {
        'form': cliente_form,
        'formset': contato_formset,
        'acao': 'Novo'
    })


# Editar cliente
@login_required
def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST, instance=cliente)
        contato_formset = ContatoFormSet(request.POST, instance=cliente)

        if cliente_form.is_valid() and contato_formset.is_valid():
            cliente_form.save()
            contato_formset.save()
            messages.success(request, f'Cliente {cliente.nome} e seus contatos foram atualizados com sucesso!')
            return redirect('cliente_list')
        else:
            # Mostrando erros detalhados
            error_messages = []

            # Erros do form principal
            for field, errors in cliente_form.errors.items():
                for error in errors:
                    error_messages.append(f"Campo '{field}': {error}")

            # Erros do formset
            for i, form in enumerate(contato_formset.forms):
                for field, errors in form.errors.items():
                    for error in errors:
                        error_messages.append(f"Contato {i+1} - Campo '{field}': {error}")

            # Envia todas as mensagens de erro
            for msg in error_messages:
                messages.error(request, msg)
    else:
        cliente_form = ClienteForm(instance=cliente)
        contato_formset = ContatoFormSet(instance=cliente)

    return render(request, 'cliente_form.html', {
        'form': cliente_form,
        'formset': contato_formset,
        'acao': 'Editar'
    })


# Excluir cliente
@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.is_excluido = True
        cliente.save()
        # cliente.delete()
        messages.success(request, f'Cliente {cliente.nome} foi excluído com sucesso!')
        return redirect('cliente_list')
    return render(request, 'cliente_confirm_delete.html', {'cliente': cliente})


# Retornar contatos dos clientes
@login_required
def cliente_contatos_ajax(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    # contatos = cliente.contatos.all().values('nome', 'telefone')
    contatos = Contato.objects.filter(cliente_id=cliente.pk).values('nome', 'telefone')
    return JsonResponse(list(contatos), safe=False)
