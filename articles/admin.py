from blogproject.articles.models import Article, Comment
from django.contrib import admin

#Pre populating slug field with title field value in admin
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
