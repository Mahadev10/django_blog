from django.shortcuts import render,redirect
from . import models
from .forms import CommnetForm
from django.db.models import Count
def defaultData():
    query_set = models.Like.objects.values('post').annotate(Count('post'))[0:3]
    id_list = map(lambda post:post['post'],query_set)
    popular_posts = models.Post.objects.filter(id__in=id_list,status="published")
    categories = models.Category.objects.all()
    tags = models.Tag.objects.all()
    return (popular_posts,categories,tags)
def home(request):
    posts = models.Post.objects.filter(status="published")
    popular_posts,categories,tags = defaultData()
    return render(request, "index.html", context={"posts": posts, "popular_posts":popular_posts,"categories": categories, "tags": tags,"alert":True})


def detailPost(request, slug):
    post = models.Post.objects.get(slug=slug)
    if request.method == "POST":
        form = CommnetForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
    if request.user.is_anonymous or request.user.comments.filter(post=post).count():
        form = None
    else:
        form = CommnetForm()
    if request.user.is_anonymous:
        liked=False
    else:
        try:
            models.Like.objects.get(post=post,user=request.user)
            liked=True
        except models.Like.DoesNotExist:
            liked = False
    popular_posts,categories,tags = defaultData()
    comments = post.comments.filter(active=True)
    return render(request, "detail.html", context={"post": post,"popular_posts":popular_posts, "categories": categories, "tags": tags, "comments": comments, "form": form,"liked":liked})

def categoryPosts(request,category_name):
    try:
        category = models.Category.objects.get(name=category_name)
        posts = category.posts.all()
    except models.Category.DoesNotExist:
        posts = None    
    popular_posts,categories,tags = defaultData()
    result_msg={"key":"Category","msg":category_name}
    return render(request, "results.html", context={"posts": posts,"popular_posts":popular_posts, "categories": categories, "tags": tags,"result_msg":result_msg})

def tagPosts(request,tag_name):
    try:
        tag = models.Tag.objects.get(name=tag_name)
        posts = tag.posts.all()
    except models.Tag.DoesNotExist:
        posts = None    
    popular_posts,categories,tags = defaultData()   
    result_msg={"key":"Tag","msg":tag_name}
    return render(request, "results.html", context={"posts": posts, "popular_posts":popular_posts,"categories": categories, "tags": tags,"result_msg":result_msg})

def likePost(request,slug):
    if request.user.is_anonymous:
        return redirect("signin")
    post = models.Post.objects.get(slug=slug)    
    try:
        like = models.Like.objects.get(post=post,user=request.user)
        like.delete()
    except:
        like = models.Like(user=request.user,post=post)
        like.save()
    return redirect("post_detail",slug)

def searchPosts(request):
    if request.method == "GET":
        search_keyword=request.GET['search_keyword']
        posts=models.Post.objects.filter(title__icontains=search_keyword)
        popular_posts,categories,tags = defaultData()   
        result_msg={"key":"Results for","msg":search_keyword}
        return render(request, "results.html", context={"posts": posts, "popular_posts":popular_posts,"categories": categories, "tags": tags,"result_msg":result_msg})