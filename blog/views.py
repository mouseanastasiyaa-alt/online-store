from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.models import BlogPost


class BlogPostListView(ListView):
    """Список опубликованных статей."""
    model = BlogPost
    template_name = "blog/blogpost_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        # Только опубликованные статьи
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    """Просмотр одной статьи. Увеличивает счётчик просмотров."""
    model = BlogPost
    template_name = "blog/blogpost_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=["views_count"])

        if obj.views_count == 100:
            self._send_congratulations(obj)

        return obj

    def _send_congratulations(self, post):
        send_mail(
            subject=f"Поздравляем! Статья «{post.title}» набрала 100 просмотров",
            message=(
                f"Ваша статья «{post.title}» достигла 100 просмотров!\n\n"
                f"Ссылка: {self.request.build_absolute_uri(post.get_absolute_url())}"
            ),
            from_email=None,   # возьмётся DEFAULT_FROM_EMAIL
            recipient_list=["admin@example.com"],   # сюда — свой email
            fail_silently=True,
        )
class BlogPostCreateView(CreateView):
    """Создание новой статьи."""
    model = BlogPost
    template_name = "blog/blogpost_form.html"
    fields = ("title", "content", "preview", "is_published")

    def get_success_url(self):
        return reverse_lazy("blog:post_detail", kwargs={"pk": self.object.pk})


class BlogPostUpdateView(UpdateView):
    """Редактирование статьи. После сохранения — редирект на статью."""
    model = BlogPost
    template_name = "blog/blogpost_form.html"
    fields = ("title", "content", "preview", "is_published")

    def get_success_url(self):
        return reverse_lazy("blog:post_detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(DeleteView):
    """Удаление статьи."""
    model = BlogPost
    template_name = "blog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")