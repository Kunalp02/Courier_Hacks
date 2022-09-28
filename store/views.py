from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Product, ReviewRating, FeaturesByProduct
from category.models import Category
from carts.models import CartItem
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct


@csrf_exempt
def store(request, category_slug=None):
    select_min = 0
    select_max = 5000
    if request.method == 'POST':
        select_min = request.POST.get('select_min')
        select_max = request.POST.get('select_max')
        print(select_min)
        print(select_max)

    # categories = None
    # products = None

    if category_slug != None:
        # it will bring categories if found other wise it will show 404 Error
        categories = get_object_or_404(Category, slug=category_slug)
        
        products = Product.objects.filter(
            category=categories, is_available=True)
        print(products)
       
        
        product_count = products.count()
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_product,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    features = FeaturesByProduct.objects.all()
    print(features)
    features_filter= FeaturesByProduct.objects.get(product_id=single_product.id)
    print(features_filter.__dict__)
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()  # we are going to check items in the cart model. It will show True or false.
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)


    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct' : orderproduct,
        'reviews' : reviews,
        'features_filter' : features_filter,
    }
    return render(request, 'store/product_detail.html', context)



def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword'] # storing the value of that keyword in the variable
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
        context = {
            'products' : products,
            'product_count' : product_count,
        }
    return render(request, 'store/store.html', context)



def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance = reviews)
            form.save()
            messages.success(request, "Thank you! Your review has been updated")
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject    = form.cleaned_data['subject']
                data.rating     = form.cleaned_data['rating']
                data.review     = form.cleaned_data['review']
                data.ip         = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id    = request.user.id
                data.save()
                messages.success(request, "Thank you! Your review has been submitted")
                return redirect(url)
            else:
                print(form.errors)
                error = ""
                print(form.errors.items())
                list_of_errors = ""
                for field, error in form.errors.items():
                    print(f'{field}:{error}')
                    list_of_errors += error
                print(list_of_errors)
                messages.warning(request, f"{list_of_errors}")
                return redirect(url)