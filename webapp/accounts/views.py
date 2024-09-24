from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from accounts.models import Product, Review
from django.shortcuts import render, get_object_or_404
from .forms import ReviewForm
def home(request):
    products = Product.objects.all()  # Fetch all products to display
    return render(request, 'home.html', {'products': products})
# views.py
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()  # ดึงรีวิวของสินค้านั้นๆ
    return render(request, 'product_detail.html', {'product': product, 'reviews': reviews})

def search(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    
    return render(request, 'search_results.html', {'products': products})

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'form': form, 'product': product})

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'form': form, 'product': product})

def signup(request):
    return render(request, "signup.html")

def login(request):
    return render(request, "login.html")

def addUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']

        if password == repassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'This username is already taken.')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already registered.')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username,
                    first_name=firstname,
                    last_name=lastname,
                    email=email,
                    password=password
                )
                user.save()
                messages.success(request, 'Registration successful!')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')
    else:
        return redirect('signup')

def loginForm(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')  # เปลี่ยนให้ไปหน้า home แทนหน้า products
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    else:
        return redirect('login')

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)  # Update the user model with instance=request.user
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('/')  # Redirect to home page after saving
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserProfileForm(instance=request.user)  # Load the user's current data in the form
    return render(request, 'profile.html', {'form': form})

@login_required
def reset_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            messages.success(request, 'Your password has been successfully updated!')
            return redirect('reset_password_complete')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = SetPasswordForm(user=request.user)
    return render(request, 'reset_password.html', {'form': form})

def reset_password_complete(request):
    return render(request, 'reset_password_complete.html')

def product_list(request):
    products = Product.objects.all()  # Fetch all products from the database
    return render(request, 'products.html', {'products': products})
