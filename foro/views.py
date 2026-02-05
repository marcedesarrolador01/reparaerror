from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post
from django.db.models import Q

def post_list(request):
    query = request.GET.get("q")
    categoria = request.GET.get("categoria")

    posts = Post.objects.filter(publicado=True)

    if query:
        posts = posts.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(marca__nombre__icontains=query) |
            Q(modelo__nombre__icontains=query)
        )

    if categoria:
        posts = posts.filter(categoria__slug=categoria)

    paginator = Paginator(posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "foro/post_list.html", {
        "page_obj": page_obj,
        "query": query
    })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, publicado=True)
    return render(request, "foro/post_detail.html", {"post": post})
