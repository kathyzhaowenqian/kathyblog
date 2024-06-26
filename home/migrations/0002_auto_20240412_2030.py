# Generated by Django 3.2 on 2024-04-12 12:30

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import minio_storage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('饲养技巧', '饲养技巧'), ('饮食习性', '饮食习性'), ('医疗保健', '医疗保健')], max_length=255, verbose_name='文章分类')),
                ('reference', models.CharField(blank=True, max_length=255, null=True, verbose_name='源链接')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
            ],
            options={
                'verbose_name_plural': '文章分类',
                'db_table': 'blogs"."BlogCategory',
            },
        ),
        migrations.CreateModel(
            name='BlogDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_detail', ckeditor_uploader.fields.RichTextUploadingField(default='', verbose_name='文章内容')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
            ],
            options={
                'verbose_name_plural': '文章详情',
                'db_table': 'blogs"."BlogDetail',
            },
        ),
        migrations.CreateModel(
            name='BlogList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='标题')),
                ('abstract', models.CharField(blank=True, max_length=255, null=True, verbose_name='摘要')),
                ('image_url', models.ImageField(storage=minio_storage.storage.MinioMediaStorage(), upload_to='blog/')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
                ('category', models.ForeignKey(db_column='category', default='饮食习性', on_delete=django.db.models.deletion.CASCADE, to='home.blogcategory', verbose_name='文章分类')),
            ],
            options={
                'verbose_name_plural': '文章列表',
                'db_table': 'blogs"."BlogList',
            },
        ),
        migrations.DeleteModel(
            name='ImageModel',
        ),
        migrations.AddField(
            model_name='blogdetail',
            name='listid',
            field=models.ForeignKey(db_column='listid', on_delete=django.db.models.deletion.CASCADE, to='home.bloglist', verbose_name='文章列表'),
        ),
    ]
