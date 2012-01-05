from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models import permalink

class Article(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return "%s" % self.title

    @permalink
    def get_absolute_url(self):
        return ('article_details', None, {'slug': self.slug})

class Comment(models.Model):
    comment_body = models.TextField()
    com_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=64, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    article = models.ForeignKey(Article)

    def __unicode__(self):
        return "%d: %s" % (self.id,self.comment_body[:20])

class ArticleForm(ModelForm):
    class Meta:
        model = Article

class CommentForm(ModelForm):
    class Meta:
        model = Comment
