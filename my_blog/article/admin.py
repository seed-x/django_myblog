from django.contrib import admin
from .models import ArticlePost
# Register your models here.
#后台中需要添加ArticlePost这个数据表供管理
admin.site.register(ArticlePost)