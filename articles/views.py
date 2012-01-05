from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from blogproject.articles.models import *
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required

#Imports required for populating slug field accurately
import re
import unicodedata
from django.utils.safestring import mark_safe

#index view renders homepage which consists of a paginated list of blog articles
def index(request):
    article_list = Article.objects.all().order_by('-pub_date')

    #Show 10 articles per page
    paginator = Paginator(article_list, 10)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        articles = paginator.page(page)
    except (EmptyPage, InvalidPage):
        articles = paginator.page(paginator.num_pages)
        
    return render_to_response('articles/index.html', {
        'article_list': articles}, context_instance=RequestContext(request))

#article_details view renders the article identified by the slug field
#along with it's comments and a form to add new comment.
def article_details(request, slug):
    article = Article.objects.get(slug=slug)
    
    total_comments = article.comment_set.count()
    
    comment_list = article.comment_set.order_by('-com_date').all()

    form = CommentForm()
    
    return render_to_response('articles/detail.html', {
            'article':article, 'total_comments':total_comments,
            'comment_list':comment_list, 'form':form},
            context_instance=RequestContext(request))

#add view renders the form to write a new blog article
@login_required
def add(request):
    if request.method == 'POST':
        data = request.POST.copy()

        #Adding user to POST data
        data['user'] = request.user.id

        #Creating slug value from title and adding it to POST data
        slug = data['title']
        slug = unicodedata.normalize('NFKD', slug).encode('ascii', 'ignore')
        slug = unicode(re.sub('[^\w\s-]', '', slug).strip().lower())
        data['slug'] = mark_safe(re.sub('[-\s]+', '-', slug))
        
        form = ArticleForm(data)
        if form.is_valid():
            new_article = form.save()
            return HttpResponseRedirect('/articles/details/'+data['slug']+'/')
    else:
        form = ArticleForm()

    return render_to_response("articles/add-edit.html", {
        'form':form}, context_instance=RequestContext(request))

#edit view renders the form for editing an existing blog article
@login_required
def edit(request, article_id=None):
    if request.method == 'POST':
        data = request.POST.copy()

        #Adding user to POST data
        data['user'] = request.user.id
        
        article_id = data['article_id']
        article = Article.objects.get(pk=article_id)
        
        form = ArticleForm(data,instance=article)
        if form.is_valid():
          form.save()
          return HttpResponseRedirect('/articles/details/'+article.slug+'/')
    else:
        article = Article.objects.get(pk=article_id)
        form = ArticleForm(instance=article)
    return render_to_response("articles/add-edit.html", {
            'form':form,'article':article},
            context_instance=RequestContext(request))

#delete view simply deletes the blog article
@login_required
def delete(request, article_id):
    article = Article.objects.get(pk=article_id)
    article.delete()
    return HttpResponseRedirect('/accounts/profile/')

#This view is called when a new comment is posted for an article        
def add_comment(request):
    if request.method == 'POST':
        data = request.POST.copy()

        if request.user.is_authenticated():
          #Adding user to POST data
          data['user'] = request.user.id    
        
        form = CommentForm(data)
        if form.is_valid():
            new_comment = form.save()
            return HttpResponseRedirect('/articles/details/'+data['slug']+'/')

#delete_comment view deletes the comment from the article.
def delete_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    slug = comment.article.slug

    comment.delete()

    return HttpResponseRedirect('/articles/details/'+slug+'/')
    


    
