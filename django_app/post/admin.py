from django.contrib import admin

# Register your models here.

# Post에 대한 ModelAdin을 만들고 register
# 이후 /admin에 가서 Post확인하고 사진 첨부
from .models import Post


class PostAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
