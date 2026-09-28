from django.shortcuts import render


def home(request):
    """Контроллер главной страницы (каталог)."""
    return render(request, "catalog/home.html")


def contacts(request):
    """Контроллер страницы контактов."""
    return render(request, "catalog/contacts.html")
