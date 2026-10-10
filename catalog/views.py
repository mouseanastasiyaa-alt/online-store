from django.shortcuts import get_object_or_404, redirect, render
from catalog.forms import ProductForm
from catalog.models import Contact, Product
from django.core.paginator import Paginator



def home(request):
    """Контроллер главной страницы (каталог)."""
    products = Product.objects.all()
    paginator = Paginator(products, 3)  # по 3 товара на страницу
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "catalog/home.html", {"page_obj": page_obj})


def contacts(request):
    """Контроллер страницы контактов с обработкой формы обратной связи."""
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        Contact.objects.create(name=name, phone=phone, message=message)

        print(f"Новое сообщение: {name} | {phone} | {message}")
        return render(request, "catalog/contacts.html", {"success": True})

    contacts_list = Contact.objects.all()
    return render(request, "catalog/contacts.html", {"contacts": contacts_list})


def product_detail(request, pk):
    """Контроллер страницы с подробной информацией о товаре."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, "catalog/product_detail.html", {"product": product})


def product_create(request):
    """Контроллер страницы добавления товара."""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect("catalog:product_detail", pk=product.pk)
    else:
        form = ProductForm()

    return render(request, "catalog/product_form.html", {"form": form})