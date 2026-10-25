from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from catalog.forms import ProductForm
from catalog.models import Contact, Product


class ProductListView(ListView):
    """Список товаров с пагинацией."""
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "page_obj"
    paginate_by = 3
    ordering = "-created_at"


class ProductDetailView(DetailView):
    """Подробная информация о товаре."""
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    """Форма добавления нового товара."""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self):
        return self.object.get_absolute_url()


class ContactsView(View):
    """Страница контактов с обработкой формы обратной связи."""

    def get(self, request):
        contacts_list = Contact.objects.all()
        return render(request, "catalog/contacts.html", {"contacts": contacts_list})

    def post(self, request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        Contact.objects.create(name=name, phone=phone, message=message)

        print(f"Новое сообщение: {name} | {phone} | {message}")
        return render(request, "catalog/contacts.html", {"success": True})