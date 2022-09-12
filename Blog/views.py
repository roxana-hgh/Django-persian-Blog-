from urllib.request import Request
from django.shortcuts import render,redirect, HttpResponse
from django.urls import reverse
from .models import Post, Comments, Followers
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentsForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from functools import wraps



def home(request, pk='latest'):
    if pk == 'latest':
        posts = Post.objects.all().order_by('-date')
        latest = 'active'
        popular = 'disactive'
    elif pk == 'popular':
        posts = Post.objects.all().order_by('-likes')
        popular = 'active'
        latest = 'disactive'

    p = Paginator(posts, 6)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    if request.user.is_authenticated:
        followings = Followers.objects.get(user = request.user).another_user.all().values('id')
        followins_posts = Post.objects.filter(author__in = followings).order_by('-date')
    return render(request, 'Blog/home.html',{'page_obj': page_obj, 'popular' : popular, 'latest' : latest, 'followins_post' : followins_posts})


def Post_view(request,pk):
    post = Post.objects.get(id=pk)
    comments = Comments.objects.filter(post= pk).order_by('-date')
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.post = post
            form.save()
            return redirect('view_post', pk = pk)
    else:
        form = CommentsForm()
    return render(request, 'Blog/post.html',{'post': post, 'comments': comments,'form': form})


def delete_comment(request):    
    comment = Comments.objects.get(id = request.GET['pk'])
    comment.delete()
    return HttpResponse("succes")    


def user_profile(request,pk): 
    author = User.objects.get(username = pk)
    posts = Post.objects.filter(author = author).order_by('-date')
    followings = Followers.objects.get(user = author).another_user.all()
    followers = Followers.objects.filter(another_user = author)
    followers_id = Followers.objects.filter(another_user = author).values_list('user',flat='true')
    p = Paginator(posts, 6)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, 'Blog/profile.html', {'page_obj': page_obj, 'user': author,
    'followings':followings, 'followers': followers, 'posts':posts, "followers_id" : followers_id  })


def follow_user(request):  
    
    follower = Followers.objects.get(user = request.user)
    target_user = User.objects.get(id= request.GET['pk'])
    follower.another_user.add(target_user)
    return HttpResponse("succes")

def unfollow_user(request):    
    target_user = User.objects.get(id= request.GET['pk'])
    follower = Followers.objects.get(user = request.user)
    follower.another_user.remove(target_user)
    return HttpResponse("succes")


def categories(request, pk):
    category = str(pk)
    posts = Post.objects.filter(category = pk).order_by('-date')
    p = Paginator(posts, 6)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, 'Blog/category.html', {'page_obj': page_obj, 'category': category})


@login_required(login_url = 'login')
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            new = form.save()
        return redirect(reverse('view_post', kwargs={'pk': new.id}))
    else:
        form = PostForm()
    context = {'form': form}
    return render(request,'Blog/new_post.html',context)


@login_required(login_url = 'login')
def update_post(request,pk):
    post = Post.objects.get(id=pk)
    
    if request.user != post.author:
        return HttpResponse("<h2>access denied!</h2>")
    
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('view_post', kwargs={'pk': pk}))
    context = {'form': form, 'item': post}
    return render(request,'Blog/update.html',context)


@login_required(login_url = 'login')
def delete(request,pk):
    post = Post.objects.get(id=pk)
    if request.user != post.author:
        return HttpResponse("<h2>access denied!</h2>")
    if request.method == 'POST':
        post.delete()
        return redirect('profile', pk = request.user)

    context = {'post': post}
    return render(request,'Blog/delete.html',context) 


def post_like(request):    
    post = Post.objects.get(id= request.GET['pk'])
    post.likes.add(request.user)
    return HttpResponse("succes")
        

def post_unlike(request):    
    post = Post.objects.get(id= request.GET['pk'])
    post.likes.remove(request.user)
    return HttpResponse("succes")


def search(request):
    keyword = request.POST.get('word')
    result = Post.objects.filter(title__contains = keyword)
    p = Paginator(result, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request,'Blog/search_result.html',{'page_obj': page_obj, 'keyword': keyword})




