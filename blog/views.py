from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Post, Comments, Category
from blog.forms import PostForm
from datetime import datetime


def post_list(request):
    posts = Post.objects.all().filter(published=True)
    category = Category.objects.all()
    counter = posts.count()
    return render(request, 'blog/post_list.html', {'items': posts,
                                                   'category': category,
                                                   'counter': counter})


def categories(request, category_pk):
    posts = Post.objects.filter(category=category_pk)
    category = Category.objects.all()
    return render(request, 'blog/post_list.html', {'items': posts,
                                                   'category': category})


def post_draft(request):
    posts = Post.objects.all().filter(published=False)
    return render(request, 'blog/post_draft.html', {'items': posts})


def published_post(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    post.published = True
    post.save()
    return render(request, 'blog/post_detail.html', {'post': post})


def post_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    comments = Comments.objects.filter(post=post_pk)
    # author = Comments.author()
    counter = comments.count()
    return render(request, 'blog/post_detail.html', {'post': post,
                                                     'comments': comments,
                                                     'counter': counter})



def post_new(request):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'blog/post_new.html', {'form': form})
    else:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_date = datetime.now()
            post.published_date = datetime.now()
            post.save()
            return redirect('post_detail', post_pk=post.pk)


def post_edit(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'GET':
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
    else:
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_date = datetime.now()
            post.published_date = datetime.now()
            post.save()
            return redirect('post_detail', post_pk=post.pk)


def post_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk).delete()
    return redirect('post_list')


