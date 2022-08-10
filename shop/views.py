from datetime import datetime
from multiprocessing import context
from django.shortcuts import render, get_object_or_404 , redirect
from shop.models import *
from django.db.models import OuterRef, Subquery ,Min
from django.db.models import F
from django.contrib import auth


# Create your views here.

def detail(request, itemId):
    product = get_object_or_404(Product, pk=itemId)
    gallery=Gallery.objects.filter(product=itemId)
    variant=VariantProduct.objects.filter(product=itemId)
    review=Review.objects.filter(product=itemId)
    context={'product': product , 'gallery':gallery,'variant':variant,'review':review}
    return render(request, 'shop/detail.html', context)

def home(request):
    if request.method == 'POST':
        pass
        # Movie.objects.filter(title__contains=request.POST['search']).order_by('add_date').reverse()
    else:
        products=Product.objects.annotate(minPrice=Min('variantproduct__mainPrice'))
        #products = Product.objects.annotate(minPrice=Subquery(VariantProduct.objects.filter(
        #    product=OuterRef("pk")).order_by("mainPrice").values("mainPrice")[:1]))
        context={'products': products}
        return render(request, 'shop/home.html',context )

def shop(request,filterby="date",filterfield="newest",showcount=12):
    if request.method == 'POST':
        pass
    else:
        categories=Category.objects.all().order_by('name')
        products=Product.objects.annotate(minPrice=Min('variantproduct__mainPrice'))
        pcount=Product.objects.all().count()
        context={'products': products , 'categories':categories,'pcount':pcount}
        return render(request, 'shop/shop.html',context )
    
def edit_cart(request):
    
    if request.method == 'POST':
        print('\033[91m' +"print:  "+ str(request.POST) + '\033[0m')
        try:
            quantity=request.POST['newvalue']
            CartItem.objects.filter(id=request.POST['cartid']).update(quantity=quantity)
        except:
            pass  
    return redirect('shoppingcart')
    
def add_to_cart(request):
    if request.method == 'POST':
        quantity=request.POST['quantityvalue']
        variant=VariantProduct.objects.get(id=request.POST['radioid'])
        try:
            shopcart = ShopCart.objects.get(user=request.user)
        except ShopCart.DoesNotExist:
            shopcart = ShopCart.objects.create(user=request.user,createDate=datetime.now())
        
        cartitem=CartItem.objects.filter(shopCart=shopcart,variantProduct=variant).update(quantity=quantity)
        if cartitem == 0:
            cartitem=CartItem.objects.create(shopCart=shopcart,variantProduct=variant,quantity=quantity,createDate=datetime.now())        
        #print('\033[91m' +"print:  "+ str(cartitem) + '\033[0m')
            
        
        return redirect('shoppingcart')
    else:
        return render(request, '')

def remove_from_cart(request):
    if request.method == 'POST':
        #variant=VariantProduct.objects.get(id=request.POST['remove'])
        #user=request.user
        CartItem.objects.filter(id=request.POST['remove']).delete()
        return redirect('shoppingcart')
    else:
        pass


def shoppingcart(request):
    shopcart=ShopCart.objects.get(user=request.user)
    cartitems=CartItem.objects.filter(shopCart=shopcart)
    totalmain=0
    totaldiscount=0
    for item in cartitems:
        totalmain=totalmain+(item.variantProduct.mainPrice*item.quantity)
        totaldiscount=totaldiscount+(item.variantProduct.discountPrice*item.quantity)
    #print('\033[91m' +"print:  main:"+ str(totalmain)+" dis: "+ str(totaldiscount) + '\033[0m')
        
    context={'cartitems' : cartitems,'totalmain':totalmain,'totaldiscount':totaldiscount}
    return render(request, 'shop/shoppingcart.html',context)
    #print('\033[91m' +"print:  "+ str(request.user.shopcart) + '\033[0m')
    
    """
    if request.method == 'POST':
        pass
        # Movie.objects.filter(title__contains=request.POST['search']).order_by('add_date').reverse()
    else:
        products=Product.objects.annotate(minPrice=Min('variantproduct__mainPrice'))
        #products = Product.objects.annotate(minPrice=Subquery(VariantProduct.objects.filter(
        #    product=OuterRef("pk")).order_by("mainPrice").values("mainPrice")[:1]))
        context={'products': products}
        return render(request, 'shop/home.html',context )
    """