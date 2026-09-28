from django.shortcuts import render


def home(recuest):
    """Контроллер главной страницы (каталог)."""
    return render(request,"catalog/home.html")


def contacts(request):
    """Контроллер страницы контактов."""
    return render(request,"catalog/contact.html")

