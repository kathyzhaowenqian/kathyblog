FROM python:3.9.12

# Set build-time environment variable lots of todo
ARG DJANGO_SECRET_KEY

ARG PG_DBNAME
ARG PG_DBUSER
ARG PG_PASSWORD
ARG PG_HOST
ARG PG_PORT

ARG APIKEY_OPENAI
ARG ORGANIZATION_OPENAI
ARG APIKEY_CLAUDE

ARG MINIO_URL
ARG MINIO_STORAGE_ENDPOINT
ARG MINIO_STORAGE_ACCESS_KEY
ARG MINIO_STORAGE_SECRET_KEY
ARG MINIO_STORAGE_MEDIA_BUCKET_NAME
 
ARG ALI_ECS_EXTERNAL_IP
ARG ALIYUN_ACCESS_ID
ARG ALIYUN_ACCESSKEY_SECRET


# Set environment variables,lots of to do
ENV DJANGO_SECRET_KEY $DJANGO_SECRET_KEY

ENV PG_DBNAME $PG_DBNAME
ENV PG_DBUSER $PG_DBUSER
ENV PG_PASSWORD $PG_PASSWORD
ENV PG_HOST $PG_HOST
ENV PG_PORT $PG_PORT

ENV APIKEY_OPENAI $APIKEY_OPENAI
ENV ORGANIZATION_OPENAI $ORGANIZATION_OPENAI
ENV APIKEY_CLAUDE $APIKEY_CLAUDE

ENV MINIO_URL $MINIO_URL
ENV MINIO_STORAGE_ENDPOINT $MINIO_STORAGE_ENDPOINT
ENV MINIO_STORAGE_ACCESS_KEY $MINIO_STORAGE_ACCESS_KEY
ENV MINIO_STORAGE_SECRET_KEY $MINIO_STORAGE_SECRET_KEY
ENV MINIO_STORAGE_MEDIA_BUCKET_NAME $MINIO_STORAGE_MEDIA_BUCKET_NAME


ENV ALI_ECS_EXTERNAL_IP $ALI_ECS_EXTERNAL_IP
ENV ALIYUN_ACCESS_ID $ALIYUN_ACCESS_ID
ENV ALIYUN_ACCESSKEY_SECRET $ALIYUN_ACCESSKEY_SECRET


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

LABEL version ="0.1"
LABEL maintainer="Kathy Zhao"

# 创建一个项目文件
RUN mkdir /kathyblog
# 创建一个 static 静态文件夹，用来存放 python manage.py collectstatic 的目录
RUN mkdir /static


# 把当前路径下的 django项目 文件夹(比如myobject1)的内容 拷贝到容器 /djangotest 文件夹下
# 注意如果是文件夹的话，这里的必须是相对路径
COPY . /kathyblog

# 进入到容器内工作目录就是 
WORKDIR /kathyblog

# 设置时间为上海时间
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# 安装 requirements.txt 模块
RUN python -m pip install --upgrade pip
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt
