---
title: readme 
date: 2020-03-06 09:20
author: zcmimi
avatar: /img/avatar.jpg
tags: 
 - readme

thumbnail: 
top: 2 
---

## 关于博客

这个博客是我用来记录各种**学习笔记**和**技术分享**的小站

## 博客引擎

基于Python

博客的生成引擎是我自己编写的,看得上的话请到github给我star一个吧?

目前的主题(当然也是默认,也还没有人开发其他主题)是我自己编写的material主题,基于[MDUI](https://mdui.org)

主要功能完成,某些小功能正在开发中

**兼容Hexo,Jekyll等静态网站生成器**,可以从无缝切换

使用markdown.

其中使用[front-matter](#front-matter)记录文章的title,date,tags等信息

## 使用说明

**建议使用前了解一下yaml的语法**

### 依赖

请先安装`python-frontmatter`

建议先将`pip`换为国内源

```bash
pip install frontmatter
```

### blog.py

核心文件

```
0. 无参数: 渲染博客,生成的文件在web文件夹中   
1. [s or server] + [port(端口号,默认8000)]: 在localhost上预览生成的文件   
2. [n or new] + [title]: 新建文章   
3. [cp or createpage] + [title]: 新建页面
```
### 配置

配置文件`config.yml`

使用yaml语法

```yaml
site_name: <your blog name> # 站点名称
blog_icon: <blog icon url> # 博客图标图片地址
avatar: <your avatar url> # 博客头像,默认头像地址
author: <your name> # 默认作者
theme: beauty # 自带主题两种风格(beauty | clean)

article_address: pinyin # 文章地址(number|pinyin)
# 若选择pinyin,需要先安装pypinyin
# pip install pypinyin

# 首页
page_articles: 10 # 每页文章数
preview_len: 100 # 每篇文章截取长度

randomimg_type: folder # 随机图片地址类型(folder | list)
randomimg_list: # 随机图片地址列表
# - url
randomimg_path: /img # 随机图片地址文件夹
randomimg_tot: 20 # 图片总数
randomimg_suf: webp # 图片后缀

htmlmin: 0 # 是否压缩源代码(1|0)
# 若填1,请先pip install htmlmin

comment_typ: valine # 目前仅支持valine

# Valine评论(请参考https://valine.js.org/configuration.html)
valine_appid: <your leancloud appid>
valine_appkey: <your leancloud appkey>
valine_placeholder: 说几句嘛qwq # 提示语
valine_visitor: 1 # 访问量
valine_notify: 1 # 是否邮件通知

```

### source

`_posts`文件夹存放文章的markdown

`_pages`文件夹存放页面的markdown或配置文件

其他文件夹会被复制到`web`文件夹(即网站)的根目录,如可以防止存放图片的`img`文件夹

### front-matter

使用yaml语法

Front-matter 是文件最上方以 --- 分隔的区域，用于指定个别文件的变量，举例来说：

```yaml
---
title: readme          # 文章标题              不填为文章的文件名
date: 2020-03-06 09:20 # 文章建立日期          不填为文章的文件修改日期
author: zcmimi         # 作者                 不填为默认作者
avatar:                # 头像                 不填为默认头像
tags:                  # 标签
  - 技术
  - readme
thumbnail: /img/0.webp # 自定义缩略图地址       不填为config中的随机图片
top: 1                 # 置顶优先级(越大越高)   不填为0
comment: 1             # 是否开启评论          不填为1
---
```

### 自定义侧边栏

请修改`layout/drawer_mb.html`

### 自定义友情链接

修改`source/_pages/links.yml`

使用yaml语法

请参考注释

### 添加自定义代码

1. 自定义`css`
   
   修改`assets/custom.css`,它会在源代码`head`部分被引入

2. 自定义`html`
   
   修改`layout/custom.html`,这部分代码会添加到源代码末尾(`</html>`的前面)


## 部署

生成的所有文件都放在`web`文件夹中，您可以将它们复制到您喜欢的地方。

推荐部署到: 

1. github pages
   
2. coding pages
   
3. netlify
   
4. 腾讯云cos
   
5. gitlab pages
   
6. 用rsync或其他工具推送到您的服务器