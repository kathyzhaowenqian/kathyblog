from django.db import models
from minio_storage.storage import MinioMediaStorage
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

from PIL import Image

from django.core.files.base import ContentFile
import io
from django.conf import settings
from minio import Minio
from minio.error import S3Error
MinioClient = Minio(settings.MINIO_STORAGE_ENDPOINT,
    access_key=settings.MINIO_STORAGE_ACCESS_KEY,
    secret_key=settings.MINIO_STORAGE_SECRET_KEY,
    secure=True  #https
)
# 要用富文本编辑器

# 博客列表页
# 标题
# 摘要
# 主图图片地址
# 分类
# reference
# create time
# update time
# is activate

class BlogCategory(models.Model):
    category_choices=(
        ('饲养技巧', '饲养技巧'),
        ('饮食习性', '饮食习性'),
        ('医疗保健', '医疗保健'),
    )
    category= models.CharField(verbose_name='文章分类',max_length=255, choices=category_choices,blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)
    class Meta:
        db_table = 'blogs\".\"BlogCategory'
        # verbose_name = '公司列表'
        verbose_name_plural = '文章分类'

    def __str__(self):
            return self.category

class BlogList(models.Model):
    title = models.CharField(verbose_name='标题',max_length=255, blank=True, null=True)
    abstract = models.TextField(verbose_name='摘要',blank=True, null=True)
    image_url = models.ImageField(verbose_name='文章主图', storage=MinioMediaStorage(), upload_to='blog/')
    category = models.ForeignKey('BlogCategory', models.CASCADE, db_column='category',to_field='id',verbose_name='文章分类')
    reference = models.CharField(verbose_name='源链接',max_length=255, blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)
    class Meta:
        db_table = 'blogs\".\"BlogList'
        # verbose_name = '公司列表'
        verbose_name_plural = '文章列表'

    def __str__(self):
            return self.title
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_image_url = self.image_url.name if self.pk else None

    def save(self, *args, **kwargs):
        if self.pk is None or self.image_url.name != self.original_image_url:
            # 获取原有的图片路径
            old_image_url = self.original_image_url
            print('old_image_url',old_image_url)

            # 检查是否是新图片
            # 打开图片
            print('self.image_url',self.image_url)
            with self.image_url.open() as img:
                img = Image.open(img)
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                img = img.resize((1000, 666), resample=Image.BICUBIC)
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG')
                buffer.seek(0)
                # 注意：这里需要使用django的ContentFile来包装buffer
                self.image_url.save(self.image_url.name, ContentFile(buffer.read()), save=False)
                buffer.close()

            # 删除原有的图片
            if old_image_url:
                try:
                    # 删除原有的图片
                    MinioClient.remove_object(settings.MINIO_STORAGE_MEDIA_BUCKET_NAME, old_image_url)
                except S3Error as exc:
                    print(f"Error deleting object: {exc}")

            # 更新原有的图片路径
            self.original_image_url = self.image_url.name
            

    # 调用模型的原生save方法
        super().save(*args, **kwargs)



        


class BlogDetail(models.Model):
    listid = models.OneToOneField('BlogList', models.CASCADE, db_column='listid',to_field='id',verbose_name='文章列表')
    article_detail = RichTextUploadingField(default='', verbose_name='文章内容')
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)
    class Meta:
        db_table = 'blogs\".\"BlogDetail'
        # verbose_name = '公司列表'
        verbose_name_plural = '文章详情'



# 博客详情页表
# 外键 列表页的id
# 标题
# 摘要
# 内容
# 图片地址
# 分类
# reference
# create time
# update time
# is activate


class Contacts(models.Model):
    name= models.CharField(verbose_name='姓名',max_length=255,blank=False, null=False)
    email= models.CharField(verbose_name='邮箱',max_length=255,blank=False, null=False)
    subject= models.CharField(verbose_name='主题',max_length=255,blank=False, null=False)
    content= models.CharField(verbose_name='内容',max_length=255,blank=False, null=False)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(verbose_name='是否呈现',null=False, default = True)
    class Meta:
        db_table = 'blogs\".\"Contacts'
        # verbose_name = '公司列表'
        verbose_name_plural = '联系我们'

    def __str__(self):
            return self.subject