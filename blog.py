import os
import sys
import time
import shutil
import json
import yaml
import random
import math
import webbrowser
from frontmatter import Frontmatter

def other(): # 其他操作
    tmp=sys.argv
    if(".py" in tmp[0]):
        cmd=[]
        for i in tmp:
            if(".py" in i): continue
            cmd.append(i)
    else: cmd=tmp
    if(len(cmd)>0):
        if(cmd[0]=="s" or cmd[0]=="server"): 
            import http.server
            import socketserver
            if(not os.path.exists("web")): 
                print("请先渲染博客")
                sys.exit()
            os.chdir("web")
            PORT=8000
            if(len(cmd)>1): PORT=int(cmd[1])
            Handler = http.server.SimpleHTTPRequestHandler
            with socketserver.TCPServer(("", PORT), Handler) as httpd:
                print("http://localhost:"+str(PORT))
                webbrowser.open("http://localhost:"+str(PORT))
                httpd.serve_forever()
        if(cmd[0]=="n" or cmd[0]=="new"):
            if(len(cmd)<2):
                print("未输入文件名!")
                sys.exit()
            info={"date":time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())),"title":cmd[1]}
            flag=1
            if(os.path.exists("source/_posts/"+cmd[1]+".md")): 
                print("文件已存在,是否覆盖(yes|No)")
                flag=0
                if(input()=="yes"):flag=1
            if(flag):open("source/_posts/"+cmd[1]+".md","w").write(open("scaffolds/post.md").read().format(**info))
        if(cmd[0]=="cp" or cmd[0]=="createpage"):
            if(len(cmd)<2):
                print("未输入文件名!")
                sys.exit()
            info={"date":time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())),"title":cmd[1]}
            flag=1
            if(os.path.exists("source/_pages/"+cmd[1]+".md")): 
                print("文件已存在,是否覆盖(yes|No)")
                flag=0
                if(input()=="yes"):flag=1
            if(flag):open("source/_pages/"+cmd[1]+".md","w").write(open("scaffolds/page.md").read().format(**info))
        if(cmd[0]=="h" or cmd[0]=="help" or cmd[0]=="-h" or cmd[0]=="--help"):
            print(
'''
0. 无参数: 渲染博客,生成的文件在web文件夹中
1. [s or server] + [port(端口号,默认8000)]: 在localhost上预览生成的文件
2. [n or new] + [title]: 新建文章
3. [cp or createpage] + [title]: 新建页面
''')
        sys.exit()

other()

config=yaml.load(open("config.yml").read())
index_mb=open("layout/index_mb.html").read()
index_node_mb=open("layout/index_node_%s.html"%config["theme"]).read()
article_mb=open("layout/article_mb.html").read()
custom_html=open("layout/custom.html").read()
drawer_mb=open("layout/drawer_mb.html").read().format(**config)
tag_mb=open("layout/tag_node_mb.html").read()
tag_pages_mb=open("layout/tag_pages_mb.html").read()
link_node_mb=open("layout/link_node_mb.html").read()
link_pages_mb=open("layout/link_pages_mb.html").read()
other_pages_mb=open("layout/other_pages_mb.html").read()
comment_mb=open("layout/comment_%s.html"%config["comment_typ"]).read().format(**config)

if(config["htmlmin"]): # 压缩源码
    import htmlmin
    index_mb=htmlmin.minify(index_mb)
    index_node_mb=htmlmin.minify(index_node_mb)
    article_mb=htmlmin.minify(article_mb)
    drawer_mb=htmlmin.minify(drawer_mb)
    custom_html=htmlmin.minify(custom_html)
    tag_mb=htmlmin.minify(tag_mb)
    tag_pages_mb=htmlmin.minify(tag_pages_mb)
    link_node_mb=htmlmin.minify(link_node_mb)
    link_pages_mb=htmlmin.minify(link_pages_mb)
    other_pages_mb=htmlmin.minify(other_pages_mb)
    comment_mb=htmlmin.minify(comment_mb)

if(config["article_address"]=="pinyin"):
    import pypinyin

config.update({"drawer":drawer_mb})
config.update({"custom_html":custom_html})

if(os.path.exists("web")): shutil.rmtree("web")
os.mkdir("web")
os.mkdir("web/tags/")
shutil.copytree("assets","web/assets")
for i in os.listdir("source"):
    if("_pages" in i or "_posts" in i):continue
    if(os.path.isdir("source/"+i)):
        shutil.copytree("source/"+i,"web/"+i)
    else:shutil.copyfile("source/"+i,"web/"+i)

data=[]
data_json=[]
all_tags={}
index_articles=""
id=0

def turn_tag_to_html(tags): #生成tag的html
    res=""
    for i in tags: res+=tag_mb.format(**{"tag":i})
    return res
def randomimg():
    if(config["randomimg_type"]=="folder"):
        return config["randomimg_path"]+'/'+str(random.randint(0,config["randomimg_tot"]-1))+"."+config["randomimg_suf"]
    else: 
        return config["randomimg_list"][random.randint(0,len(config["randomimg_list"])-1)]

def geninfo(dir,file): # 获取文件信息
    node=Frontmatter.read_file(dir+file)
    info=node['attributes']

    article=""
    if("body" in node and node["body"]!=None):article=node["body"]

    if(info!=None and "thumbnail" in info and info["thumbnail"]!=None):thumbnail=info["thumbnail"]
    else:thumbnail=randomimg()

    if(info!=None and "title" in info and info["title"]!=None):title=info["title"]
    else:title=file[0:len(file)-3]
    print(title)

    if(info!=None and "tags" in info and info["tags"]!=None):tags=info["tags"]
    else:tags=[]

    if(info!=None and "author" in info and info["author"]!=None):author=info["author"]
    else:author=config["author"]

    if(info!=None and "date" in info and info["date"]!=None):date=str(info["date"])
    else:date=time.strftime('%Y-%m-%d %H:%M',time.localtime(os.stat(dir+file).st_mtime))

    top=0
    if(info!=None and "top" in info and info["top"]!=None): top=info["top"]

    istop=""
    if(top>0): istop="[置顶]"

    comment=comment_mb
    if(info!=None and "comment" in info and info["comment"]==0):comment="作者关闭了评论"

    return{
        "id":None,
        "title":title,
        "author":author,
        "thumbnail":thumbnail,
        "article":article,
        "preview": article[0:config["preview_len"]],
        "link":None,
        "tags":tags,
        "tagshtml":turn_tag_to_html(tags),
        "top":top,
        "istop": istop,
        "date":date,
        "comment": comment,
        "pre_link":None,
        "pre_title":None,
        "nxt_link":None,
        "nxt_title":None}

for i in os.listdir("source/_posts"):
    if(not i.endswith(".md")): continue
    data.append(geninfo("source/_posts/",i))

tot=len(data)

def cmp1(x): # 日期排序
    return x["date"]
def cmp2(x): # 置顶
    if(x["top"]>0):return "23333-12-31 "+str(x["top"])
    else: return x["date"]

data.sort(key=cmp1,reverse=True)

def topinyin(word):
    res=""
    for i in pypinyin.pinyin(word,style=pypinyin.NORMAL):
        res+=''.join(i)+"-"
    return res[0:len(res)-1].replace(' ','-')
id=tot
for x in data: # 按日期编号
    id-=1
    x["id"]=id
    if(config["article_address"]=="number"):x["link"]="/posts/%d"%id
    else:x["link"]="/posts/"+topinyin(x["title"])
id=0
for x in data: # 获取前后信息
    id+=1
    x["pre_link"]=data[(id-2+tot)%tot]["link"]
    x["pre_title"]=data[(id-2+tot)%tot]["title"]
    x["nxt_link"]=data[id%tot]["link"]
    x["nxt_title"]=data[id%tot]["title"]

data.sort(key=cmp2,reverse=True)

# 分页
def split_pages():
    num=config["page_articles"]
    if(math.ceil(id/num)==1): pre='#'
    elif(math.ceil(id/num)==2): pre='/'
    else: pre="/page/%d"%(math.ceil(id/num)-1)
    if(math.ceil(id/num)<math.ceil(tot/num)):nxt="/page/%d"%(math.ceil(id/num)+1)
    else: nxt='#'

    global index_articles
    res=index_mb.format(**{**config,**{"articles":index_articles,"pre":pre,"now":str(math.ceil(id/num))+'/'+str(math.ceil(tot/num)),"nxt":nxt}})
    index_articles=""

    if(math.ceil(id/num)==1): open("web/index.html","w").write(res)
    else:
        os.makedirs("web/page/%d"%math.ceil(id/num))
        open("web/page/%d/index.html"%math.ceil(id/num),"w").write(res)

id=0
for x in data:
    id+=1
    if(id%config["page_articles"]==0):split_pages()
    # 添加到首页
    res=index_node_mb.format(**{**config,**x})
    index_articles+=res
    for tag in x["tags"]:
        if tag in all_tags:all_tags[tag]+=res
        else: all_tags.update({tag:res})

    # 文章页面
    os.makedirs("web"+x["link"])
    res=article_mb.format(**{**config,**x})

    open("web"+x["link"]+"/index.html","w").write(res)
    data_json.append({"title":x["title"],"text":x["article"],"link":x["link"],"tags":x["tags"]})

split_pages()

# 生成除文章外页面
def gen_pages():
    for i in os.listdir("source/_pages/"):
        if(not i.endswith(".md")): continue
        x=geninfo("source/_pages/",i)
        res=other_pages_mb.format(**{**config,**x})
        i=i[0:len(i)-3]
        os.makedirs("web/"+i)
        open("web/"+i+"/index.html","w").write(res)
        data.append({"text":x["article"],"link":"/"+i,"title":x["title"],"tags":x["tags"]})

        for tag in x["tags"]:
            if tag in all_tags:all_tags[tag]+=res
            else: all_tags.update({tag:res})

gen_pages()

open("web/data.json","w").write(json.dumps(data_json))

#标签云和各标签页面
def gen_tagcloud():
    #标签云
    tag_cloud=""
    for tag in all_tags: tag_cloud+="<a href='/tags/"+tag+".html' class='mdui-chip mdui-text-color-black'><span class='mdui-chip-title'>"+tag+"</span><div class='mdui-chip-icon'>"+str(all_tags[tag].count("mdui-card article"))+"</div></a>"
    tag_page_mb=tag_pages_mb.format(**{**config,**{"tag_cloud":tag_cloud}})
    res=tag_page_mb.replace("{%ARTICLES%}",'')

    open("web/tags/index.html","w").write(res)

    # 生成各标签页面
    for tag in all_tags:
        res=tag_page_mb.replace("{%ARTICLES%}",all_tags[tag])
        open("web/tags/"+tag+".html","w").write(res)

gen_tagcloud()

# 生成友情链接
def gen_links():
    if(not os.path.exists("source/_pages/links.yml")):return
    link_data=yaml.load(open("source/_pages/links.yml").read())
    res=""
    for item in link_data:
        if(item=="comment"): continue
        res+="<div class='mdui-subheader'>%s</div><div class='links-row mdui-row-xs-2 mdui-row-sm-3 mdui-row-md-4 mdui-row-lg-6'>"%item
        for node in link_data[item]:
            res+=link_node_mb.format(**node)
        res+="</div>"
    comment=comment_mb
    if(link_data["comment"]==False): comment="作者以关闭评论"
    os.mkdir("web/links")
    open("web/links/index.html","w").write(link_pages_mb.format(**{**config,**{"links":res,"comment": comment}}))

gen_links()