from django.shortcuts import render

def cadastro_view(request):
    return render(request, 'cadastro.html')

def movimentacao_view(request):
    return render(request, 'movimentacao.html')

def relatorios_view(request):
    return render(request, 'relatorios.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Produto
from .forms import ProdutoForm



from django.http import JsonResponse
from .models import Produto, TipoProduto, Unidade
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Listagem
def produto_list(request):
    produtos = Produto.objects.select_related('tipo_produto').order_by('descricao')
    return render(request, 'produto_list.html', {'produtos': produtos})

# Criar
def produto_create(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Novo Produto cadastrado com sucesso!')
            return redirect('produto_list')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = ProdutoForm()
    return render(request, 'produto_form.html', {'form': form, 'acao': 'Novo'})

# Editar
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