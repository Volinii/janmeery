import markdown
from .models import Post
from django.shortcuts import render
from django.shortcuts import get_object_or_404
# Create your views here.
from django.http import HttpResponse
from pure_pagination.mixins import PaginationMixin

import re
# def index(request):
#     return render(request,
#                   'blog/index.html',
#                   context={
#                       'title': '我的博客首页',
#                       'welcome': '欢迎访问我的博客首页'
#                   })

from django.shortcuts import render
from .models import Category
from .models import Tag
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.generic import ListView, DetailView


class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10


class CategoryView(IndexView):

    # def index(request):
    #     post_list = Post.objects.all().order_by('-created_time')
    #     return render(request, 'blog/index.html', context={'post_list': post_list})
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)

        m = re.search(
            r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''

        return post


def about(request):
    return render(request, 'blog/about.html')


# class AboutView(ListView):
#     template_name = 'blog/about.html'


# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     # 阅读量 +1
#     post.increase_views()

#     md = markdown.Markdown(extensions=[
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         'markdown.extensions.toc',
#     ])
#     post.body = md.convert(post.body)
#     post.toc = md.toc
#     return render(request, 'blog/detail.html', context={'post': post})


# def ArchiveView(ListView):
#     model = Post
#     template_name = 'blog/index.html'
#     context_object_name = 'post_list'


def archive(request, year, month):
    post_list = Post.objects.filter(
        created_time__year=year,
        created_time__month=month).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


# def category(request, pk):
#     # 记得在开始部分导入 Category 类
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate).order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})


def tag(request, pk):
    # 记得在开始部分导入 Tag 类
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
