from .models import Article
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import redirect

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

# Create your views here.
def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404

def create_post(request):
    if request.user.is_authenticated:
        # Здесь будет основной код представления
        if request.method == "POST":
            # обработать данные формы, если метод POST
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }
            # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"] and not Article.objects.filter(title=form["title"]).exists():
                # если поля заполнены без ошибок
                Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                return redirect('get_article', article_id=Article.objects.get(text=form["text"], title=form["title"], author=request.user).id)
                # перейти на страницу поста
            else:
                # если введенные данные некорректны
                if Article.objects.filter(title=form["title"]).exists() and not (form["text"] and form["title"]):
                    form['errors'] = u"Название статьи не уникально!\nНе все поля заполнены!"
                elif Article.objects.filter(title=form["title"]).exists():
                    form['errors'] = u"Название статьи не уникально!"
                else:
                    form['errors'] = u"Не все поля заполнены!"
                # print(Article.objects.filter(title='dsfsf').exists())
                return render(request, 'create_post.html', {'form': form})
        else:
        # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_post.html', {})
    else:
        raise Http404
