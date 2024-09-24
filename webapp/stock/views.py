from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, Order, Review  # Combined imports for Product and Cart
import stripe
from .forms import ProductForm
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

# Function to view cart
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)  # Fetch related reviews
    return render(request, 'product_detail.html', {'product': product, 'reviews': reviews})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # ตรวจสอบว่าผู้ใช้ล็อกอินหรือไม่
    if request.user.is_authenticated:
        # สร้าง Cart ถ้ายังไม่มี
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # รับจำนวนสินค้าที่ผู้ใช้กรอก
        quantity = int(request.POST.get('quantity', 1))

        # เพิ่มสินค้าลงในตะกร้า
        # ถ้ามีสินค้านั้นอยู่แล้ว ให้เพิ่มปริมาณ
        existing_item = cart.products.filter(id=product.id).first()
        if existing_item:
            existing_item.quantity += quantity  # สมมติว่ามีฟิลด์ quantity ใน CartItem หรือคล้ายคลึงกัน
            existing_item.save()
        else:
            cart.products.add(product, through_defaults={'quantity': quantity})  # สมมติว่ามีการใช้ through model ที่ชื่อว่า CartItem
        cart.save()
        return redirect('cart')  # เปลี่ยนเป็น URL ของหน้า ตะกร้า
    return redirect('login')  # เปลี่ยนเป็น URL ของหน้า เข้าสู่ระบบ

def cart(request):
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
        return render(request, 'cart.html', {'cart': cart})
    return redirect('login')