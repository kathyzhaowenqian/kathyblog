from django.contrib import admin
# from minio_storage.utils import remove_file
# Register your models here.
from home.models import *
# Register your models here.
# 页面标题
admin.site.site_title="阿呆阿瓜网站后台管理系统"

# 登录页导航条和首页导航条标题
admin.site.site_header="阿呆阿瓜网站后台管理系统"

# 主页标题
admin.site.index_title="欢迎你"



# class BlogDetailInLine(admin.TabularInline):
#     model = BlogDetail
#     fields=['project','company'] 



class BlogDetailInline(admin.TabularInline):
    model = BlogDetail
    fk_name = "listid"
    extra = 0
    fields =['article_detail']


@admin.register(BlogCategory)  
class BlogCategoryAdmin(admin.ModelAdmin):   
     exclude = ('id','createtime','updatetime','is_active')



@admin.register(BlogList)  
class BlogListAdmin(admin.ModelAdmin):   
    inlines=[BlogDetailInline]
    exclude = ('id','createtime','updatetime','is_active')
    required = ('image_url',)


@admin.register(BlogDetail)  
class BlogDetailAdmin(admin.ModelAdmin):   
    exclude = ('id','createtime','updatetime','is_active')


@admin.register(Contacts)  
class ContactsAdmin(admin.ModelAdmin):   
    list_display=['name','email','subject','content','createtime']
    exclude = ('id','createtime','updatetime','is_active')
