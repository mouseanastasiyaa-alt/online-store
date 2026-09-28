from django.shortcuts import render


def home(request):
    """Контроллер главной страницы (каталог)."""
    return render(request, "catalog/home.html")


def contacts(request):
    """Контроллер страницы контактов с обработкой формы обратной связи."""
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        # Здесь в будущем можно сохранять данные в БД или отправлять email.
        # Пока просто выведем в консоль сервера, чтобы убедиться, что данные дошли.
        print(f"Новое сообщение: {name} | {phone} | {message}")

        return render(request, "catalog/contacts.html", {"success": True})

    return render(request, "catalog/contacts.html")