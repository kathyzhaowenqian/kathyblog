from django.shortcuts import render
from django.views import View
from django.http import JsonResponse,HttpResponse
from django.conf import settings
from minio import Minio
from django.shortcuts import redirect
import json
from home.models import *
from datetime import datetime


MinioClient = Minio(settings.MINIO_STORAGE_ENDPOINT,
    access_key=settings.MINIO_STORAGE_ACCESS_KEY,
    secret_key=settings.MINIO_STORAGE_SECRET_KEY,
    secure=False
)
# Create your views here.
class MainPage(View):
    def get(self,request):
        bucket=settings.MINIO_STORAGE_MEDIA_BUCKET_NAME
        minio_url = settings.MINIO_URL
        blog_articles = BlogList.objects.values('id', 'title', 'abstract', 'image_url').order_by('-createtime')[:10]
        
        for article in blog_articles:
            abstract = article['abstract']
            if len(abstract) > 50:
                article['abstract'] = f"{abstract[:50]}..."
        blog_articles = list(blog_articles)
        return render(request, 'index.html',locals())
    
 
class GET_KNOWLEDGELIST(View):
    def get(self, request):
        bucket=settings.MINIO_STORAGE_MEDIA_BUCKET_NAME
        minio_url = settings.MINIO_URL
        blog_articles = BlogList.objects.values('id', 'title', 'abstract', 'image_url').order_by('-createtime')[:10]
        
        for article in blog_articles:
            abstract = article['abstract']
            if len(abstract) > 50:
                article['abstract'] = f"{abstract[:50]}..."
        serialized_articles = list(blog_articles)
        return JsonResponse({'blog_articles': serialized_articles,'bucket':bucket,'minio_url':minio_url})
    

class ABOUT(View):
    def get(self,request):
        bucket=settings.MINIO_STORAGE_MEDIA_BUCKET_NAME
        minio_url = settings.MINIO_URL
        return render(request, 'about.html',locals())

class PROJECT(View):
    def get(self,request):
        minio_url = settings.MINIO_URL
        bucket=settings.MINIO_STORAGE_MEDIA_BUCKET_NAME
        return render(request, 'project.html',locals())
    
class GALLERY(View):
    def get(self,request):
        minio_url = settings.MINIO_URL
        
        # 从这里从图片数据库里拉取图片的url地址，然后再返回给前端页面，前端页面根据业务逻辑，下拉加载。
        bucket='kathyblog-gallery'
        folder='ai-chinchilla-watermark'
        objects = MinioClient.list_objects(bucket,prefix=folder, recursive=True)
        # 列出存储桶中的对象

        # 对对象根据上传时间进行排序
        sorted_objects = sorted(objects, key=lambda obj: obj.last_modified, reverse=True)

        # 获取最新的10张图片
        latest_images = sorted_objects[:300]
        testobj=list(latest_images)
        print(testobj)
       
        image_path_list=[]
        for i in testobj:
            full_file_path = f'{minio_url}/{bucket}/{i.object_name}'
            image_path_list.append(full_file_path)
        # print(image_path_list)
        minio_img_url_list = json.dumps(image_path_list)
        
        return render(request, 'gallery.html',locals())

class KNOWLEDGE(View):
    def get(self,request):
        minio_url = settings.MINIO_URL
        bucket=settings.MINIO_STORAGE_MEDIA_BUCKET_NAME
        blog_list = BlogList.objects.values('id', 'title', 'abstract','image_url','category__category','reference','createtime').order_by('-createtime')

        # 将结果转换为所需的格式
        result1 = [{'id': item['id'],'title': item['title'],'abstract': item['abstract'], 'image_url': f'{minio_url}/{bucket}/'+item['image_url'],'category': item['category__category'],'reference': item['reference'],'date' : item['createtime'].strftime("%Y年%m月%d日")} for item in blog_list]
        # print(result1)
        result = json.dumps(result1)
        return render(request, 'knowledge.html', locals())



class KNOWLEDGE_DETAILS(View):
    def get(self,request, pk):
        minio_url = settings.MINIO_URL
        bucket=settings.MINIO_STORAGE_MEDIA_BUCKET_NAME

        blog_list = BlogList.objects.get(id = pk)
        blogdetails=blog_list.blogdetail.article_detail
        result ={'title': blog_list.title,'abstract': '摘要：'+blog_list.abstract, 'image_url': f'{minio_url}/{bucket}/'+str(blog_list.image_url) ,'category': blog_list.category.category ,'reference': blog_list.reference, 'date' : blog_list.createtime.strftime("%Y年%m月%d日"), 'blogdetails':blogdetails}
        # print(result)
        # result = json.dumps(result1)
        return render(request, 'knowledgedetails.html', result)




class PostDetails(View):
    def get(self,request):
        return render(request, 'knowledgedetails.html')


class CONTACT(View):
    def get(self,request):
        return render(request, 'contact.html')  

class CONTACTS(View):
    def post(self,request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        content = request.POST.get('message')
        print('返回值',name,email,subject,content)
        Contacts.objects.create(name=name, email=email, subject=subject, content=content)


        # 返回JSON响应
        return JsonResponse({'success': True})


class DRAGON_GAME(View):
    def get(self,request):
        return redirect('https://www.chinchillatown.com:6501')
    

class TEST(View):
    def get(self,request):
        minio_url = settings.MINIO_URL
        
        # 从这里从图片数据库里拉取图片的url地址，然后再返回给前端页面，前端页面根据业务逻辑，下拉加载。
        bucket='kathyblog-gallery'
        folder='ai-chinchilla-watermark'
        objects = MinioClient.list_objects(bucket,prefix=folder, recursive=True)
        obj_list=list(objects)
        # print(obj_list)
        testobj=obj_list[:10]
        image_path_list=[]
        for i in testobj:
            full_file_path = f'{minio_url}/{bucket}/{i.object_name}'
            image_path_list.append(full_file_path)
        # print(image_path_list)
        minio_img_url_list = json.dumps(image_path_list)
        return render(request, 'test.html',locals())  

# from .models import ImageModel
# from django.core.files.storage import default_storage

class TEST2(View):

    def get(self,request):
        return render(request, 'uploadimagetest.html')
    
    def post(self,request):
 
        image_file = request.FILES['image']
        image = ImageModel(image=image_file)
        image.save()
        

