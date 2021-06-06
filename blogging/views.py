from django.http.response import Http404, HttpResponse
from django.shortcuts import render, redirect
from django import forms
from django.utils import timezone
from django.template import loader
from blogging.models import Post
from blogging.forms import MyPostForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


def stub_view(request, *args, **kwargs):
    body = "Stub View\n\n"
    if args:
        body += "Args:\n"
        body += "\n".join(["\t%s" % a for a in args])
    if kwargs:
        body += "Kwargs:\n"
        body += "\n".join(["\t%s: %s" % i for i in kwargs.items()])
    return HttpResponse(body, content_type="text/plain")


def add_model(request):

    if request.method == "POST":
        form = MyPostForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            # model_instance.published_date = timezone.now()
            model_instance.save()
            return redirect("/")
    else:
        form = MyPostForm()
        return render(request, "add.html", {"form": form})


class PostListView(ListView):
    queryset = Post.objects.exclude(published_date__exact=None)
    post_list = queryset.order_by("-published_date")
    template_name = "list.html"


class PostDetailView(DetailView):
    queryset = Post.objects.exclude(published_date__exact=None)
    template_name = "blogging/detail.html"
