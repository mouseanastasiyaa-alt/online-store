from django.shortcuts import render

from catalog.models import Contact, Product


def home(request):
    """Контроллер главной страницы (каталог)."""
    latest_products = Product.objects.order_by("-created_at")[:5]
    for product in latest_products:
        print(f"{product.name} — {product.price}")
    return render(request, "catalog/home.html", {"latest_products": latest_products})


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
