
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from shop.models import *
from django.db.models import Min
from django.core.paginator import Paginator
from django.utils.encoding import uri_to_iri
from django.db.models import F
import requests

# Create your views here.
API_KEY='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzM4NCJ9.eyJ0b2tlbl9pZCI6ODcxNywicGF5bG9hZCI6bnVsbH0.30IGA2q8-tQBjIp0YETAM77cad8qoF3SgAFBKVzvk10gubOGr-r95z77tA7CStcY'

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
        popularProducts = Product.objects.annotate(minPrice=Min('variantproduct__mainPrice')).order_by('-averageRating')[0:4]
        newProducts = Product.objects.annotate(minPrice=Min('variantproduct__mainPrice')).order_by('-createDate')[0:4]
        mostVisitedProducts = Product.objects.annotate(minPrice=Min('variantproduct__mainPrice')).order_by('-ratingCount')[0:4]
        # fix to mostVisitedProducts = Product.objects.annotate(minPrice=Min('variantproduct__mainPrice')).order_by('view')[0:4]
        

        context = {'newProducts': newProducts,'mostVisitedProducts': mostVisitedProducts,'popularProducts': popularProducts,}
        return render(request, 'shop/home.html', context)


def shop(request, filterby="date", filterfield="CreateDate", showcount=12):
    if request.method == 'POST':
        pass
    else:
        if(filterby == "category"):
            filterfield = uri_to_iri(filterfield)
            products = Product.objects.filter(category__name=filterfield).annotate(minPrice=Min(
                'variantproduct__mainPrice'))
        elif(filterby == "price"):
            filterfield = filterfield.split(',')
            filterfield[0] = int(filterfield[0])*1000
            filterfield[1] = int(filterfield[1])*1000
            products = Product.objects.annotate(minPrice=Min('variantproduct__mainPrice')).filter(
                minPrice__lte=filterfield[1], minPrice__gte=filterfield[0])
        elif(filterby == "size"):
            products = Product.objects.annotate(minPrice=Min(
                'variantproduct__mainPrice')).filter(variantproduct__size=filterfield)

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
    if(request.POST):
        try:
            if(request.POST['update'] == 'on'):
                User.objects.filter(username=request.user).update(
                    first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'])
                Profile.objects.filter(user=request.user).update(mobilePhone=request.POST['mobilephone'],
                                address=request.POST['address'],city=request.POST['city'],
                                postalCode=request.POST['postalcode'], phone=request.POST['phone'])

            cartitems = CartItem.objects.filter(shopCart__user=request.user)
            informations = "name :"+request.POST['fname']+" "+request.POST['lname']+"\n address" + \
                request.POST['city']+',  '+request.POST['address'] + "\npostal code :"+request.POST['postalcode'] + \
                "\n mobilephone :"+request.POST['mobilephone']+" , phone :" + \
                request.POST['phone']+"\nemail :"+request.POST['email']+"\n"
            order = Order.objects.create(user=request.user, createDate=datetime.now()
                                        , informations=informations, note=request.POST['note'])

            for cartitem in cartitems:
                OrderItem.objects.create(order=order, variantProduct=cartitem.variantProduct,
                                         price=cartitem.variantProduct.discountPrice, status='o')
                VariantProduct.objects.filter(id=cartitem.variantProduct.id).update(quantity=F('quantity')-cartitem.quantity)
                CartItem.objects.filter(id=cartitem.id).delete()

                ''' API for decrease quantity on digikala

                url = f"https://seller.digikala.com/api/v1/variants/{cartitem.variantProduct.dkpc}/"
                payload = f"{{\n    \"seller_stock\": {VariantProduct.objects.get(id=cartitem.variantProduct.id).quantity} }}"
                headers = {
                    'Authorization': API_KEY
                }
                response = requests.request("PUT", url, headers=headers, data=payload)
                
                '''
            return redirect('shoppingcart')

        except Exception as e:
            print('\033[91m' + "print EXCEPTION :  " + str(e) + '\033[0m')

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
                   'totaldiscount': totaldiscount }
        return render(request, 'shop/order.html', context)