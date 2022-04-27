from django.shortcuts import render, get_object_or_404
from .models import Category, Products
from django.core.paginator import Paginator, InvalidPage, EmptyPage


# Create your views here.

def index(request):
    return render(request, 'index.html')


def allProdCat(request, c_slug=None):
    c_page = None
    product_list = None
    if c_slug is not None:
        c_page = get_object_or_404(Category, slug=c_slug)
        product_list = Products.objects.all().filter(category_model=c_page, available=True)
    else:
        product_list = Products.objects.all().filter(available=True)
    paginator = Paginator(product_list, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = Paginator.page(paginator.num_pages)
    return render(request, 'category.html', {'category': c_page, 'products': products})


def poductDetails(request, c_slug, p_slug):
    try:
        product = Products.objects.get(category_model__slug=c_slug, slug=p_slug)
    except Exception as e:
        raise e
    return render(request, 'product.html', {'product': product})
