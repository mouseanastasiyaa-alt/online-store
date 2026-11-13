from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from catalog.forms import ProductForm
from catalog.models import Contact, Product
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from catalog.services import get_products_by_category


class ProductListView(ListView):
    """Список товаров с пагинацией."""
    model = Product
    template_name = "catalog/home.html"
    paginate_by = 3
    ordering = "-created_at"


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Подробная информация о товаре."""
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    @method_decorator(cache_page(60 * 15))  # кеш на 15 минут
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Форма добавления нового товара."""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование товара."""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user and not self.request.user.has_perm("catalog.can_unpublish_product"):
            raise PermissionDenied("Вы не можете редактировать чужой продукт.")
        return obj

    def get_success_url(self):
        return self.object.get_absolute_url()


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление товара."""
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("catalog:home")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user and not self.request.user.has_perm("catalog.can_unpublish_product"):
            raise PermissionDenied("Вы не можете удалять чужой продукт.")
        return obj


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


class CategoryProductsView(ListView):
    """Список продуктов в указанной категории."""
    template_name = "catalog/category_products.html"
    context_object_name = "products"

    def get_queryset(self):
        category_id = self.kwargs["pk"]
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from catalog.models import Category
        context["category"] = Category.objects.get(pk=self.kwargs["pk"])
        return context