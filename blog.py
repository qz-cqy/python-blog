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

config=yaml.load(open("config.yml",encoding='utf-8').read())

def mkdir(path):
    if(not os.path.exists(path)): os.makedirs(path)

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
            if(flag):open("source/_posts/"+cmd[1]+".md","w",encoding='utf-8').write(open("scaffolds/post.md").read().format(**info))
        if(cmd[0]=="np" or cmd[0]=="newpage"):
            if(len(cmd)<2):
                print("未输入文件名!")
                sys.exit()
            info={"date":time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())),"title":cmd[1]}
            flag=1
            if(os.path.exists("source/_pages/"+cmd[1]+".md")):
                print("文件已存在,是否覆盖(yes|No)")
                flag=0
                if(input()=="yes"):flag=1
            if(flag):open("source/_pages/"+cmd[1]+".md","w",encoding='utf-8').write(open("scaffolds/page.md").read().format(**info))
        if(cmd[0]=="d" or cmd[0]=="deploy"):
            if not os.path.exists('web'):
                print("请先渲染博客")
                sys.exit()
            import git
            if os.path.exists('deploy'):
                repo=git.Repo.init('deploy')
            else:
                print("Clone...")
                repo=git.Repo.clone_from(url=config['repo'], to_path='deploy')
                open('deploy/.gitignore','w',encoding='utf-8').write('.git')
            for i in os.listdir('deploy'):
                if '.git' in i: continue
                if os.path.isdir('deploy/'+i): shutil.rmtree('deploy/'+i)
                else: os.remove('deploy/'+i)
            for i in os.listdir('web'):
                if i=='.git': continue
                if os.path.isdir('web/'+i): shutil.copytree('web/'+i,'deploy/'+i)
                else: shutil.copy('web/'+i,'deploy/'+i)

            os.chdir('deploy')
            repo.git.add('.')
            print(repo.git.commit(m='.'))
            print(repo.remote().push())


        if(cmd[0]=="h" or cmd[0]=="help" or cmd[0]=="-h" or cmd[0]=="--help"):
            print(
'''
0. 无参数: 渲染博客,生成的文件在web文件夹中
1. [s/server] + [port(端口号,默认8000)]: 在localhost上预览生成的文件
2. [n/new] + [title]: 新建文章
3. [np/newpage] + [title]: 新建页面
4. [d/deploy]: 部署博客
''')
        sys.exit()

other()

if(config["assets_rt"]==None or config["assets_rt"]==""):
    config["assets_rt"]=config["site_rt"]+"/assets"

index_mb=open("layout/index_mb.html",encoding='utf-8').read()
index_node_mb=open("layout/index_node_%s.html"%config["theme"],encoding='utf-8').read()
article_mb=open("layout/article_%s.html"%config["theme"],encoding='utf-8').read()
tag_mb=open("layout/tag_node_mb.html",encoding='utf-8').read()
tag_number_mb=open("layout/tag_node_number_mb.html",encoding='utf-8').read()
tag_pages_mb=open("layout/tag_pages_mb.html",encoding='utf-8').read()
categories_node_mb=open("layout/categories_node_mb.html",encoding='utf-8').read()
categories_pages_mb=open("layout/categories_pages_mb.html",encoding='utf-8').read()
link_node_mb=open("layout/link_node_mb.html",encoding='utf-8').read()
link_pages_mb=open("layout/link_pages_mb.html",encoding='utf-8').read()
other_pages_mb=open("layout/other_pages_mb.html",encoding='utf-8').read()
comment_mb=open("layout/comment_%s.html"%config["comment_typ"],encoding='utf-8').read().format(**config)
rt=config["site_rt"]

head=open("layout/head.html",encoding='utf-8').read().format(**config)

def gen_drawer():
    res=\
'''
<div class="mdui-drawer mdui-drawer-close mdui-drawer-full-height mdui-shadow-2" id="drawer">
    <ul class="mdui-list">
        <div class="mdui-list-item mdui-ripple">
            <i class="mdui-list-item-icon mdui-icon material-icons mdui-text mdui-text-color-black">home</i>
            <a href="{site_rt}/" class="mdui-list-item-content">{site_name}</a>
        </div>
        <a href="{site_rt}/about">
            <img class='avatar mdui-shadow-1' src="{avatar}" width="90%" height="90%" style="margin: 10px;"></img>
        </a>
'''
    info=yaml.load(open("source/drawer.yml",encoding='utf-8').read())
    for i in info:
        res+="<li class='mdui-subheader'>%s</li>"%i
        for j in info[i]:
            if(j['icon_typ']=='mdui'):
                icon="<i class='mdui-list-item-icon mdui-icon material-icons mdui-text-color-%s'>%s</i>"%(j['icon_color'],j['icon'])
            else:
                icon='''<img class='mdui-list-item-icon' src="%s">'''%j['icon']
            res+=\
'''
<li class="mdui-list-item mdui-ripple">
    %s<a href="%s" class="mdui-list-item-content">%s</a>
</li>
'''%(icon,j['url'],j['content'])
    return res

if(os.path.exists("source/drawer.yml")): drawer=gen_drawer().format(**config)
else: drawer=open("source/drawer.html",encoding='utf-8').read().format(**config)

pjax=open("layout/pjax.html",encoding='utf-8').read().format(**config) if config['pjax'] else ''
music=open("layout/music.html",encoding='utf-8').read().format(**config)
search=open("layout/search.html",encoding='utf-8').read().format(**config)
appbar=open("layout/appbar.html",encoding='utf-8').read().format(**config)
custom_html=open("layout/custom.html",encoding='utf-8').read()

if(config["htmlmin"]): # 压缩源码
    import htmlmin
    index_mb=htmlmin.minify(index_mb)
    index_node_mb=htmlmin.minify(index_node_mb)
    article_mb=htmlmin.minify(article_mb)
    tag_mb=htmlmin.minify(tag_mb)
    tag_number_mb=htmlmin.minify(tag_number_mb)
    tag_pages_mb=htmlmin.minify(tag_pages_mb)
    link_node_mb=htmlmin.minify(link_node_mb)
    link_pages_mb=htmlmin.minify(link_pages_mb)
    other_pages_mb=htmlmin.minify(other_pages_mb)
    comment_mb=htmlmin.minify(comment_mb)

    head=htmlmin.minify(head)
    drawer=htmlmin.minify(drawer)
    pjax=htmlmin.minify(pjax)
    music=htmlmin.minify(music)
    appbar=htmlmin.minify(appbar)
    search=htmlmin.minify(search)
    custom_html=htmlmin.minify(custom_html)

if(config["article_address"]=="pinyin"):
    import pypinyin

mod={
    "head":head,
    "drawer":drawer,
    "pjax":pjax,
    "music":music,
    "appbar":appbar,
    "search":search,
    "custom_html":custom_html,
}

def turn_tag_to_html(tags): #生成tag的html
    res=""
    for i in tags: res+=tag_mb.format(**{**config,**{"tag":i}})
    return res
def randomimg():
    if(config["randomimg_type"]=="folder"):
        return config["randomimg_path"]+'/'+str(random.randint(0,config["randomimg_tot"]-1))+"."+config["randomimg_suf"]
    else:
        return config["randomimg_list"][random.randint(0,len(config["randomimg_list"])-1)]

def geninfo(dir,file): # 获取文件信息
    node=Frontmatter.read(open(dir+file,encoding='utf-8').read())
    info=node['attributes']

    article=""
    if("body" in node and node["body"]!=None):article=node["body"]

    if(info!=None and "thumbnail" in info and info["thumbnail"]!=None):thumbnail=info["thumbnail"]
    else:thumbnail=randomimg()

    if(info!=None and "title" in info and info["title"]!=None):title=info["title"]
    else:title=file[0:len(file)-3]
    # print(title)

    if(info!=None and "tags" in info and info["tags"]!=None):tags=info["tags"]
    else:tags=[]

    if(info!=None and "categories" in info and info["categories"]!=None):categories=info["categories"]
    else:categories=[]

    if(info!=None and "author" in info and info["author"]!=None):author=info["author"]
    else:author=config["author"]

    if(info!=None and "date" in info and info["date"]!=None):date=str(info["date"])
    else:date=time.strftime('%Y-%m-%d %H:%M',time.localtime(os.stat(dir+file).st_mtime))

    top=0
    if(info!=None and "top" in info and info["top"]!=None): top=info["top"]

    istop=""
    if(top>0): istop="[置顶]"

    comment=comment_mb
    if(("comment" in config and config["comment"]==False) or (info!=None and "comment" in info and info["comment"]==0)):comment="评论已关闭"

    html=""
    if(info!=None and "html" in info and info["html"]!=None):html=info["html"]

    return{
        "id":None,
        "title":title,
        "author":author,
        "thumbnail":thumbnail,
        "article":article,
        "preview": article[0:config["preview_len"]],
        "link":None,
        "categories":categories,
        "tags":tags,
        "tagshtml":turn_tag_to_html(tags),
        "top":top,
        "istop": istop,
        "date":date,
        "comment": comment,
        "pre_link":None,
        "pre_title":None,
        "nxt_link":None,
        "nxt_title":None,
        "html":html}

def topinyin(word):
    res=""
    for i in pypinyin.pinyin(word,style=pypinyin.NORMAL):
        res+=''.join(i)+"-"
    return res[0:len(res)-1].replace(' ','-')

def gen_index(path,RES,mb,ext={}):
    num=config["page_articles"]
    tmp=""
    tot=len(RES)
    TOT=math.ceil(tot/num)
    for now in range(1,TOT+1):
        tmp=''
        for i in range((now-1)*num,min(now*num,tot)):tmp+=RES[i]

        pre=path+"/page/%d"%(now-1)
        pre_ban=''
        if(now==1):
            pre='#'
            pre_ban='disabled'
        if(now==2):pre=rt+path+'/'

        nxt=path+"/page/%d"%(now+1)
        nxt_ban=''
        if(now==TOT):
            nxt='#'
            nxt_ban='disabled'

        if(now==1):
            index=path
            mkdir("web"+path)
        else:
            index=path+"/page/%d"%now
            mkdir("web"+index)
        open("web"+index+"/index.html","w",encoding='utf-8').write(mb.format(**{
            **config,**mod,**ext,
            **{
                "articles":tmp,
                "pre":pre,
                "now":str(now)+'/'+str(TOT),
                "nxt":nxt,
                'pre_ban': pre_ban,
                'nxt_ban': nxt_ban,
                'split_hide':'hidden' if TOT<2 else ""
            }
        }))
        urls.append(config["site_domain"]+rt+index)

# 生成除文章外页面
def gen_pages():
    for i in os.listdir("source/_pages/"):
        if(not i.endswith(".md")): continue
        x=geninfo("source/_pages/",i)
        res=other_pages_mb.format(**{**config,**mod,**x})
        i=i[0:len(i)-3]
        os.makedirs("web/"+i)
        open("web/"+i+"/index.html","w",encoding='utf-8').write(res)
        data_json.append({"text":x["article"],"link":rt+"/"+i,"title":x["title"],"tags":x["tags"]})
        urls.append(config["site_domain"]+rt+"/"+i)

#标签云和各标签页面
def gen_tagcloud():
    #标签云
    mkdir("web/tags")
    tag_cloud=""
    for tag in all_tags:
        tag_cloud+=tag_number_mb.format(**{**config,**{'tag':tag,'num':str(len(all_tags[tag]))}})
    open("web/tags/index.html","w",encoding='utf-8').write(tag_pages_mb.format(**{
        **config,**mod,
        **{
            "tag_cloud":tag_cloud,
            'articles':'',
            'split_hide':'hidden',
            'pre':'#','pre_ban':'',
            'nxt':'#','nxt_ban':'',
            'now':''
        }
    }))

    # 生成各标签页面
    for tag in all_tags:
        gen_index("/tags/"+tag,all_tags[tag],tag_pages_mb,{'tag_cloud':tag_cloud})

def categories_path_to_link(path):
    path=path.split('/')
    res=""
    now=rt
    for x in path:
        if(x==""):continue
        now+="/"+x
        res+="/<a href='"+now+"'>"+x+"</a>"
    return res
def gen_categories(path,now):
    categories=""
    for node in now:
        if(node=='res' or node=='cnt'):continue
        categories+=categories_node_mb.format(**{"url":rt+path+'/'+node,"name":node,"cnt":now[node]["cnt"]})
        gen_categories(path+'/'+node,now[node])
    if("res" not in now):now.update({"res":[""]})
    gen_index(path,now['res'],categories_pages_mb,{"categories":categories,"path":categories_path_to_link(path)})

# 生成友情链接
def gen_links():
    if(not os.path.exists("source/_pages/links.yml")):return
    link_data=yaml.load(open("source/_pages/links.yml",encoding='utf-8').read())
    res=""
    for item in link_data:
        if(item=="comment" or item=="info"): continue
        res+="<div class='mdui-subheader'>%s</div><div class='links-row mdui-row-xs-2 mdui-row-sm-3 mdui-row-md-4 mdui-row-lg-6'>"%item
        for node in link_data[item]:
            res+=link_node_mb.format(**node)
        res+="</div>"
    comment=comment_mb
    if(config['comment']==False or link_data["comment"]==False): comment="评论已关闭"
    mkdir("web/links")
    open("web/links/index.html","w",encoding='utf-8').write(link_pages_mb.format(**{
        **config,**mod,
        **{
            "links":res,
            "comment": comment,
            "info":link_data["info"]
        }
    }))
    urls.append(config["site_domain"]+"/links")

def gen_rss():
    import PyRSS2Gen
    import datetime
    rss_items=[]

    for i in data_json:
        link="https://"+config['site_domain']+rt+i["link"]
        text=i["text"][0:config["preview_len"]]
        res=''
        text=text.split('\n\n')
        for x in text: res+='<p>'+x+'</p>'
        res+="<a href=%s target='_blank'>阅读全文</a>"%link
        rss_items.append(PyRSS2Gen.RSSItem(
            title=i["title"],
            link=link,
            description=res,
            guid=PyRSS2Gen.Guid(link)
        ))
    rss=PyRSS2Gen.RSS2(
        title=config['site_name'],
        link="https://"+config['site_domain']+rt,
        description=config['site_name'],
        lastBuildDate=datetime.datetime.now(),
        items=rss_items
    )
    rss.write_xml(open("web/atom.xml","w"),encoding="UTF-8")

def baidu_push():
    print("是否百度推送?y|N")
    if input()!="y": return
    import requests
    print("百度推送中……")
    r=requests.post(config["baidu_push_url"],files={'file': open('web/urls.txt','rb')})
    result="推送结果:\n%s\n"%(r.text)
    print(result)

#############################################################

st_time=time.time()

if(os.path.exists("web")): shutil.rmtree("web")
mkdir("web")
shutil.copytree("assets","web/assets")
for i in os.listdir("source"):
    if("_pages" in i or "_posts" in i):continue
    if(os.path.isdir("source/"+i)):
        shutil.copytree("source/"+i,"web/"+i)
    else:shutil.copyfile("source/"+i,"web/"+i)

data=[]
data_json=[]
urls=[]
all_tags={}
all_categories={}
index_articles=[]

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

for x in data:
    # 添加到首页
    res=index_node_mb.format(**{**config,**x})
    index_articles.append(res)

    # 添加到标签页面
    for tag in x["tags"]:
        if tag in all_tags:all_tags[tag].append(res)
        else: all_tags.update({tag:[res]})

    # 添加到分类页面
    for node in x["categories"]:
        now=all_categories
        for categories in node:
            if not "cnt" in now: now.update({"cnt":1})
            else: now["cnt"]+=1
            if not categories in now: now.update({categories:{}})
            now=now[categories]
        if("res" not in now):now.update({"res":[res]})
        else: now["res"].append(res)
        if not "cnt" in now: now.update({"cnt":1})
        else: now["cnt"]+=1

    # 文章页面

    if os.path.exists('source/_posts/'+x['title']):
        shutil.copytree('source/_posts/'+x['title'],'web'+x['link']+'/')
    else:
        os.makedirs("web"+x["link"])
    res=article_mb.format(**{**config,**mod,**x})

    open("web"+x["link"]+"/index.html","w",encoding='utf-8').write(res)


    data_json.append({"title":x["title"],"text":x["article"],"link":rt+x["link"],"tags":x["tags"]})
    urls.append(config["site_domain"]+rt+x["link"])

gen_index("",index_articles,index_mb)
gen_pages()
open("web/assets/data.json","w",encoding='utf-8').write(json.dumps(data_json))
gen_tagcloud()
gen_categories("/categories",all_categories)
gen_links()
if config["rss"]: gen_rss()
urls_txt=open("web/urls.txt","w",encoding='utf-8')
for i in urls: urls_txt.write("https://"+i+'\n')

ed_time=time.time()

print("渲染使用时间: %.2fs"%(ed_time-st_time))

if config["baidu_push"]: baidu_push()