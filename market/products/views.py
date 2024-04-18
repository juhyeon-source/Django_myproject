from django.shortcuts import render, redirect
from .models import Article

def product_list(request):
    articles = Article.objects.all().order_by('-id')
    context = {"articles" : articles,}
    return render(request, 'products/product_list.html', context)

def new(request):
    return render(request, 'products/new.html')

def create(request):
    title = request.POST.get('title')
    content = request.POST.get('content')

    article = Article(title=title, content=content)
    article.save()
    return redirect('products:product_list')




