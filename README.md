# Hello Word
---
### 地址
[https://word.kathyf3.com/](https://word.kathyf3.com/)

### 开发流程

1. 将master分支pull到本地，**创建自己的分支**进行代码改动

```shell
git checkout -b *** # 自己的分支名
```

2. 创建并开启虚拟环境

```shell
python3 -m venv venv
# on linux or OS X:
source venv/bin/activate 
# on Windows:
# venv/Scripts/activate
```

3. 安装依赖

```shell
pip3 install -r requirements.txt
```

​    如果提示超时错误的话尝试以下命令，使用镜像安装：

```shell
pip3 install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
```

4. 本地运行

```shell
python3 manage.py makemigrations 
python3 manage.py migrate
python3 manage.py runserver
```
