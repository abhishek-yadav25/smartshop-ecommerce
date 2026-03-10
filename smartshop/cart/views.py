from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Cart
from products.models import Product
from django.contrib.auth.models import User
import razorpay
from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail


def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'products/product_detail.html', {'product': product})




@login_required(login_url='login')
def cart_page(request):
    cart = request.session.get('cart', [])

    total = 0
    for item in cart:
        item_total = item['price'] * item['quantity']
        item['total'] = item_total
        total += item_total

    request.session['cart_count'] = len(cart)

    return render(request, 'cart.html', {
        'cart_items': cart,
        'total': total
    })


@login_required(login_url='login')
def add_to_cart(request, name, price):

    price = float(price)

    item_id = random.randint(1000, 9999)

    cart_item = {
        'id': item_id,
        'name': name,
        'price': price,
        'quantity': 1
    }

    cart = request.session.get('cart', [])

    existing_item = None
    for item in cart:
        if item['name'] == name:
            existing_item = item
            break

    if existing_item:
        existing_item['quantity'] += 1
    else:
        cart.append(cart_item)

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


@login_required(login_url='login')
def increase_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


@login_required(login_url='login')
def decrease_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


@login_required(login_url='login')
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

def register(request):

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()
        messages.success(request, "Account created successfully")

        return redirect('login')

    return render(request, 'register.html')


def user_login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect('home')

def register(request):

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exists")
            return redirect('register')

        User.objects.create_user(username=username,email=email,password=password)

        messages.success(request,"Account created successfully")
        return redirect('login')

    return render(request,'register.html')

def checkout(request):

    total = 500

    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")

        user_email = request.user.email

        send_mail(
            "SmartShop Order Confirmation",
            f"Hello {name}, your order has been placed successfully.\n\nDelivery Address:\n{address}, {city} - {pincode}",
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
        )

        return redirect("home")

    return render(request,"checkout.html",{"total":total})

