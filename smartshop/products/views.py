from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .models import Product
import random
from django.shortcuts import redirect
from django.contrib.auth.models import User
import razorpay
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'product_detail.html', {'product': product})

@login_required(login_url='login')
def add_to_cart(request, id):

    product = Product.objects.get(id=id)

    cart = request.session.get('cart', [])

    # check if product already exists
    found = False

    for item in cart:
        if item['id'] == product.id:
            item['quantity'] += 1
            found = True
            break

    if not found:
        cart.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': 1
        })

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def cart_page(request):

    cart = request.session.get('cart', [])

    total = 0

    for item in cart:
        item['total'] = item['price'] * item['quantity']
        total += item['total']

    return render(request, 'cart.html', {
        'cart_items': cart,
        'total': total
    })


def increase_quantity(request, id):

    cart = request.session.get('cart', [])

    for item in cart:
        if item['id'] == id:
            item['quantity'] += 1

    request.session['cart'] = cart
    return redirect('cart')


def decrease_quantity(request, id):

    cart = request.session.get('cart', [])

    for item in cart:
        if item['id'] == id:
            item['quantity'] -= 1

            if item['quantity'] <= 0:
                cart.remove(item)

    request.session['cart'] = cart
    return redirect('cart')


def remove_from_cart(request, id):

    cart = request.session.get('cart', [])

    cart = [item for item in cart if item['id'] != id]

    request.session['cart'] = cart

    return redirect('cart')

def register(request):

    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        # create new user
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'register.html')



def user_login(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid login")

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def checkout(request):
    cart = request.session.get('cart', [])

    total = 0

    for item in cart:
        total += item['price'] * item['quantity']



    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    # Create Razorpay order
    payment = client.order.create({
        "amount": total * 100,   # Razorpay uses paise
        "currency": "INR",
        "payment_capture": 1
    })

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")
        payment_method = request.POST.get("payment_method")

        # Send confirmation email
        send_mail(
            "SmartShop Order Confirmation",
            f"""
Hello {name},

Your order has been placed successfully.

Delivery Address:
{address}
{city} - {pincode}

Payment Method: {payment_method}

Thank you for shopping with us!
            """,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=True
        )

        # Success popup
        messages.success(request, "Order placed successfully!")

        return redirect("home")

    return render(request, "checkout.html", {
        "payment": payment,
        "key": settings.RAZORPAY_KEY_ID,
        "total": total
    })

def search(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, 'search_results.html', {
        'products': products,
        'query': query
    })