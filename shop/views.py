from datetime import datetime
from multiprocessing import context
from re import A
import re
from django.shortcuts import render, get_object_or_404, redirect
from shop.models import *
from django.db.models import Min
from django.core.paginator import Paginator
from django.utils.encoding import uri_to_iri

# Create your views here.


def detail(request, itemId):
    product = get_object_or_404(Product, pk=itemId)
    gallery = Gallery.objects.filter(product=itemId)
    variant = VariantProduct.objects.filter(product=itemId)
    review = Review.objects.filter(product=itemId)
    context = {'product': product, 'gallery': gallery,
               'variant': variant, 'review': review}
    return render(request, 'shop/detail.html', context)


def home(request):
    if request.method == 'POST':
        pass
        # Movie.objects.filter(title__contains=request.POST['search']).order_by('add_date').reverse()
    else:
        products = Product.objects.annotate(
            minPrice=Min('variantproduct__mainPrice'))
        # products = Product.objects.annotate(minPrice=Subquery(VariantProduct.objects.filter(
        #    product=OuterRef("pk")).order_by("mainPrice").values("mainPrice")[:1]))
        context = {'products': products}
        return render(request, 'shop/home.html', context)


def shop(request, filterby="date", filterfield="CreateDate", showcount=12):
    if request.method == 'POST':
        pass
    else:
        if(filterby == "category"):
            filterfield = uri_to_iri(filterfield)
            products = Product.objects.filter(category__name=filterfield)
        elif(filterby == "price"):
            filterfield = filterfield.split(',')
            filterfield[0] = int(filterfield[0])*1000
            filterfield[1] = int(filterfield[1])*1000
            products = Product.objects.annotate(minPrice=Min('variantproduct__mainPrice')).filter(
                minPrice__lte=filterfield[1], minPrice__gte=filterfield[0])
        elif(filterby == "size"):
            products = Product.objects.annotate(minPrice=Min(
                'variantproduct__mainPrice')).filter(variantproduct__size=filterfield)
            print('\033[91m' + "print:  " + str(products) + '\033[0m')

        else:
            products = Product.objects.annotate(
                minPrice=Min('variantproduct__mainPrice'))
        pcount = Product.objects.all().count()
        paginator = Paginator(products, 3)
        page = request.GET.get('page', '1')
        products = paginator.page(page)
        categories = Category.objects.all().order_by('name')
        sizes = VariantProduct.objects.values(
            'size').order_by('size').distinct()
        print('\033[91m' + "print:  " + str(sizes) + '\033[0m')

        context = {'products': products, 'categories': categories,
                   'pcount': pcount, 'sizes': sizes}
        return render(request, 'shop/shop.html', context)


def edit_cart(request):

    if request.method == 'POST':
        #print('\033[91m' +"print:  "+ str(request.POST) + '\033[0m')
        try:
            quantity = request.POST['newvalue']
            CartItem.objects.filter(
                id=request.POST['cartid']).update(quantity=quantity)
            print('\033[91m' + "print:  " + str(request.POST) + '\033[0m')

        except:
            pass
    return redirect('shoppingcart')


def add_to_cart(request):
    if request.method == 'POST':
        if str(request.user) == 'AnonymousUser':
            print('\033[91m' + "print:  " + str(str(request.user)) + '\033[0m')
        else:
            quantity = request.POST['quantityvalue']
            variant = VariantProduct.objects.get(id=request.POST['radioid'])
            try:
                shopcart = ShopCart.objects.get(user=request.user)
            except ShopCart.DoesNotExist:
                shopcart = ShopCart.objects.create(
                    user=request.user, createDate=datetime.now())

            cartitem = CartItem.objects.filter(
                shopCart=shopcart, variantProduct=variant).update(quantity=quantity)
            if cartitem == 0:
                cartitem = CartItem.objects.create(
                    shopCart=shopcart, variantProduct=variant, quantity=quantity, createDate=datetime.now())
            #print('\033[91m' +"print:  "+ str(cartitem) + '\033[0m')
            return redirect('shoppingcart')
    else:
        return redirect('detail')


def remove_from_cart(request):
    if request.method == 'POST':
        # variant=VariantProduct.objects.get(id=request.POST['remove'])
        # user=request.user
        CartItem.objects.filter(id=request.POST['remove']).delete()
        return redirect('shoppingcart')
    else:
        pass


def shoppingcart(request):
    shopcart = ShopCart.objects.get(user=request.user)
    cartitems = CartItem.objects.filter(shopCart=shopcart)
    totalmain = 0
    totaldiscount = 0
    for item in cartitems:
        totalmain = totalmain+(item.variantProduct.mainPrice*item.quantity)
        totaldiscount = totaldiscount + \
            (item.variantProduct.discountPrice*item.quantity)

    #print('\033[91m' +"print:  main:"+ str(totalmain)+" dis: "+ str(totaldiscount) + '\033[0m')

    context = {'cartitems': cartitems, 'totalmain': totalmain,
               'totaldiscount': totaldiscount}
    return render(request, 'shop/shoppingcart.html', context)
    #print('\033[91m' +"print:  "+ str(request.user.shopcart) + '\033[0m')


def order(request):
    try:
        if(request.POST):
            #print('\033[91m' +"print:  "+ str(request.POST) + '\033[0m')
            print('\033[91m' + "print:  " +
                  str(request.user.first_name) + '\033[0m')
            address = request.POST['city']+'  '+request.POST['address']
            cartitems = CartItem.objects.filter(shopCart__user=request.user)
            informations = "name :"+request.POST['fname']+" "+request.POST['lname']+"\n address" + \
                address + "\npostal code :"+request.POST['postalcode'] + \
                "\n mobilephone :"+request.POST['mobilephone']+" , phone :" + \
                request.POST['phone']+"\nemail :"+request.POST['email']+"\n"
            order = Order.objects.create(user=request.user, createDate=datetime.now(
            ), informations=informations, note=request.POST['note'])

            if(request.POST['update'] == 'on'):
                User.objects.filter(username=request.user).update(
                    first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'])
                Profile.objects.filter(user=request.user).update(mobilephone=request.POST['mobilephone'],
                                                                 address=address, postalCode=request.POST['postalcode'], phone=request.POST['phone'])

            for cartitem in cartitems:
                OrderItem.objects.create(order=order, variantProduct=cartitem.variantProduct,
                                         price=cartitem.variantProduct.discountPrice, status='o')
                CartItem.objects.get(id=cartitem.id).delete()
    except:
        pass

        return redirect('shoppingcart')
    else:
        shopcart = ShopCart.objects.get(user=request.user)
        cartitems = CartItem.objects.filter(shopCart=shopcart)
        totalmain = 0
        totaldiscount = 0
        for item in cartitems:
            totalmain = totalmain+(item.variantProduct.mainPrice*item.quantity)
            totaldiscount = totaldiscount + \
                (item.variantProduct.discountPrice*item.quantity)
        context = {'cartitems': cartitems, 'totalmain': totalmain,
                   'totaldiscount': totaldiscount}
        return render(request, 'shop/order.html', context)

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
