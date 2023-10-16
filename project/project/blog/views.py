from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import ArticleForm, LoginForm, RegistrationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q


def index(request):
    articles = Article.objects.all()
    sort_field = request.GET.get('sort')

    if sort_field:
        articles = articles.order_by(sort_field)

    context = {
        'title': 'Главная страница',
        'articles': articles
    }

    return render(request, 'blog/index.html', context)


def category_page(request, category_id):
    articles = Article.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    sort_field = request.GET.get('sort')

    if sort_field:
        articles = articles.order_by(sort_field)
    context = {
        'articles': articles
    }

    return render(request, 'blog/index.html', context)


def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    article.views += 1
    article.save()
    articles = Article.objects.all()
    articles = articles.order_by('-views')

    context = {
        'article': article,
        'articles': articles[:4]
    }

    return render(request, 'blog/article_detail.html', context)


def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = Article.objects.create(**form.cleaned_data)
            article.save()
            return redirect('article', article.pk)
    else:
        form = ArticleForm()

    context = {
        'form': form,
        'title': 'Добавить статью'
    }

    return render(request, 'blog/article_form.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Вы успкшно авторизавались!')
                return redirect('index')
            else:
                messages.error(request, 'Не верное имя пользователя или пароль!')
                return redirect('login')
        else:
            messages.error(request, 'Не верное имя пользователя или пароль!')
    else:
        form = LoginForm()

        context = {
            'form': form,
            'title': 'Авторизация'
        }

        return render(request, 'blog/user_login.html', context)


def user_logout(request):
    logout(request)
    messages.warning(request, 'Вы вышли из аккаунта!')
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Регистрация прошла успешно")
            return redirect('login')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('register')
    else:
        form = RegistrationForm()

    context = {
        'form': form,
        'title': 'Регистрация'
    }

    return render(request, 'blog/register.html', context)


def search_results(request):
    word = request.GET.get('q')
    articles = Article.objects.filter(
        Q(title__icontains=word) | Q(content__icontains=word)
    )
    context = {
        'articles': articles
    }
    return render(request, 'blog/index.html', context)


def update_article(request, id):
    instance = Article.objects.get(id=id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('article', id)
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('update', id)
    else:
        form = ArticleForm(instance=instance)

    context = {
        'title': 'Обновление статьи',
        'form': form
    }
    return render(request, 'blog/article_form.html', context)


def delete_article(request, id):
    article = Article.objects.get(id=id)
    if request.method == 'POST':
        article.delete()
        return redirect('index')
    context = {
        'article': article
    }
    return render(request, 'blog/task_confirm_delete.html', context)


def about_me(request):
    return render(request, 'blog/about_me.html')
