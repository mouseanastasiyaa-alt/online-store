from django.shortcuts import get_object_or_404, render

from catalog.models import Contact, Product


def home(request):
    """Контроллер главной страницы (каталог)."""
    products = Product.objects.all()
    return render(request, "catalog/home.html", {"products": products})


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