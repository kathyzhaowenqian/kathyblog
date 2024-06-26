# Generated by Django 3.2 on 2024-04-12 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_blogcategory_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogcategory',
            name='reference',
        ),
        migrations.AddField(
            model_name='bloglist',
            name='reference',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='源链接'),
        ),
        migrations.AlterField(
            model_name='bloglist',
            name='category',
            field=models.ForeignKey(db_column='category', on_delete=django.db.models.deletion.CASCADE, to='home.blogcategory', verbose_name='文章分类'),
        ),
    ]
