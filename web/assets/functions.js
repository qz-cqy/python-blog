document.onreadystatechange=function(){
    if(getCookie("theme")=="night"&&document.getElementById('nightmode').innerHTML=="")night();
    else setCookie("theme","day");
    NProgress.start();
}
window.onload=function(){
    NProgress.done();
    md_turn("md_source","md_out");
    gentoc("md_out");
    var avatarurl="{%AVATAR%}",url=window.location.href,x;
    if(avatarurl.indexOf("http")==-1)avatarurl="http://"+window.location.host+avatarurl;
    x=document.getElementById("share_weibo")
    x.href=x.href.replace("_url_",url).replace("_avatar_",avatarurl);
    x=document.getElementById("share_qq");
    x.href=x.href.replace("_url_",url).replace("_avatar_",avatarurl);
    x=document.getElementById("share_twitter");
    x.href=x.href.replace("_url_",url);
}
function MD_TURN(text){
    var list=text.split("$$"),res="";
    for(i in list){
        if(i&1)res+=katex.renderToString(list[i],{displayMode:true});
        else{
            var LIST=list[i].split('$'),now="";
            for(j in LIST){
                if(j&1)now+='<latex>'+katex.renderToString(LIST[j])+'</latex>';
                else now+=LIST[j];
            }
            res+=marked(now);
        }
    }return res;
}
function md_turn(input,output){
    window.document.getElementById(output).innerHTML=MD_TURN(window.document.getElementById(input).value.trim());
    document.querySelectorAll('pre code').forEach((block)=>{hljs.highlightBlock(block);});
    hljs.initCopyButtonOnLoad();
    hljs.initLineNumbersOnLoad();
}

function gentoc(id){
    var toc=document.getElementById("toc"),
        content=document.getElementById(id),
        item=content.firstElementChild,
        secondtoc,thirdtoc;
    while(item){
        if(item.tagName=='H1'){
            var catalogA = document.createElement("a");
            catalogA.textContent=item.textContent;
            catalogA.href='#'+item.id;
            secondtoc=document.createElement("ul");
            var catalogLi=document.createElement("li");
            catalogLi.style.marginBottom = "16px";
            catalogLi.appendChild(catalogA);
            catalogLi.appendChild(secondtoc);
            toc.appendChild(catalogLi);
        }
        else if(item.tagName=='H2'){
            if(!secondtoc){
                secondtoc=document.createElement("ul");
                toc.appendChild(secondtoc);
            }
            var catalogA=document.createElement("a");
            catalogA.textContent=item.textContent;
            catalogA.href='#'+item.id;
            thirdtoc=document.createElement("ul");
            var catalogLi=document.createElement("li");
            catalogLi.appendChild(catalogA);
            catalogLi.appendChild(thirdtoc);
            secondtoc.appendChild(catalogLi);
        }
        else if(item.tagName=='H3'){
            if(!thirdtoc){
                thirdtoc=document.createElement("ul");
                toc.appendChild(thirdtoc);
            }
            var catalogA=document.createElement("a");
            catalogA.textContent=item.textContent;
            catalogA.href='#'+item.id;
            var catalogLi=document.createElement("li");
            catalogLi.appendChild(catalogA);
            thirdtoc.appendChild(catalogLi);
        }
        item=item.nextElementSibling;
        if(!item)break;
    };
}

var timeOut,speed=0;
window.onscroll=function(){
    if(document.documentElement.scrollTop>=300)document.getElementById("totop").classList.remove("mdui-fab-hide");
    else document.getElementById("totop").classList.add("mdui-fab-hide");
}
function totop(){
    if(document.body.scrollTop!=0||document.documentElement.scrollTop!=0){
        window.scrollBy(0,-(speed+=20));
        timeOut=setTimeout('totop()',20);
    }
    else clearTimeout(timeOut),document.getElementById("totop").classList.add("mdui-fab-hide"),speed=0;
}

function setCookie(cname,cval,exdays=0.5){
    var d=new Date();
    d.setTime(d.getTime()+(exdays*24*60*60*1000));
    var expires="expires="+d.toUTCString();
    document.cookie=cname+"="+cval+";"+expires+";path=/";
}
function getCookie(cname){
    var name=cname+"=",decodedCookie=decodeURIComponent(document.cookie),ca=decodedCookie.split(';'),c;
    for(i in ca){
        c=ca[i];
        while(c.charAt(0)==' ')c=c.substring(1);
        if(c.indexOf(name)==0)return c.substring(name.length, c.length);
    }return "";
}
function night(){
    if(document.getElementById('nightmode').innerHTML==""){
        setCookie("theme","night");
        document.cookie=document.cookie.replace("daymode","nightmode");
        document.querySelector('html').classList.add("mdui-theme-layout-dark");
        document.querySelector('body').classList.add("mdui-theme-layout-dark");
        document.getElementById('nightmode').innerHTML="<style>\
            .mdui-color-white{background-color: #0000 !important;color: #fff !important;}\
            .mdui-text-color-black{color: #fff !important;}\
            code{background-color: #0000 !important;color: #66ccff}\
            .vinput{color: #fff !important;}</style>"
        var hl=document.createElement('link');
        hl.href="/assets/nord.min.css";
        hl.type='text/css';
        hl.rel='stylesheet';
        document.getElementById('nightmode').appendChild(hl);
    }else{
        setCookie("theme","day");
        document.cookie=document.cookie.replace("nightmode","daymode");
        document.getElementById('nightmode').innerHTML="";
        document.querySelector('html').classList.remove("mdui-theme-layout-dark");
        document.querySelector('body').classList.remove("mdui-theme-layout-dark");
    }
}
function copylink(){
    var x=document.createElement("p"),url=window.location.href,selection=window.getSelection(),range=document.createRange();selection.removeAllRanges();
    x.innerHTML=url;x.id="share_copy_link";document.body.appendChild(x);
    range.selectNodeContents(document.getElementById('share_copy_link'));selection.addRange(range);
    document.execCommand('copy');selection.removeAllRanges();x.remove();mdui.snackbar({message: "复制成功!",position: "top"});
}