# Generated by Django 3.2 on 2024-04-17 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_bloglist_abstract'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='姓名')),
                ('email', models.CharField(max_length=255, verbose_name='邮箱')),
                ('subject', models.CharField(max_length=255, verbose_name='主题')),
                ('content', models.CharField(max_length=255, verbose_name='内容')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
            ],
            options={
                'verbose_name_plural': '联系我们',
                'db_table': 'blogs"."Contacts',
            },
        ),
    ]