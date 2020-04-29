---
title: Tools
date: 2020-03-03
html: |
    <script>
    function chk(){
        var node=document.getElementById('input_number'),x=node.value;
        if(isNaN(x)||x<0){mdui.alert('请输入有效数字!');node.value="";return;}
        if(x<=1){mdui.alert(x.toString()+'不是质数');return;}
        for(i=2;i*i<=x;++i)if(x%i==0){
            mdui.alert(x.toString()+'不是质数,可以被'+i.toString()+'整除');
            return;
        }
        mdui.alert(x.toString()+'是质数!');
    }
    </script>
---

<ul class="mdui-list">
    <li class="mdui-list-item mdui-ripple">
        <img class="mdui-list-item-icon" src="https://csacademy.com/static/favicon.png">
        <a href="https://csacademy.com/app/graph_editor/" target="_blank" class="mdui-list-item-content">根据数据生成图或树</a>
    </li>
    <li class="mdui-list-item mdui-ripple">
        <img class="mdui-list-item-icon" src="/assets/icon/markdown.svg">
        <a href="https://stackedit.io" target="_blank" class="mdui-list-item-content">在线markdown(支持latex)</a>
    </li>
    <li class="mdui-list-item mdui-ripple">
        <i class="mdui-list-item-icon mdui-icon material-icons mdui-text-color-black">edit</i>
        <a href="http://latex.codecogs.com/eqneditor/editor.php" target="_blank" class="mdui-list-item-content">在线LaTeX编辑器</a>
    </li>
    <li class="mdui-list-item mdui-ripple">
        <img class="mdui-list-item-icon" src="/assets/icon/geogebra.ico">
        <a href="https://www.geogebra.org/graphing" target="_blank" class="mdui-list-item-content">在线数学绘图</a>
    </li>
    <li class="mdui-list-item mdui-ripple">
        <i class="mdui-list-item-icon mdui-icon material-icons mdui-text-color-black">content_paste</i>
        <a href="https://paste.ubuntu.com" target="_blank" class="mdui-list-item-content">贴代码</a>
    </li>
    <li class="mdui-list-item mdui-ripple">
        <i class="mdui-list-item-icon mdui-icon material-icons" style="color: #ff4081">queue_music</i>
        <a href="/music" class="mdui-list-item-content">歌单下载器</a>
    </li>
    <li class="mdui-list-item mdui-ripple">
        <i class="mdui-list-item-icon mdui-icon material-icons mdui-text-color-blue">info</i>
        <a href="/readme" class="mdui-list-item-content">关于博客生成器</a>
    </li>
    <li class="mdui-list-item mdui-ripple">
        <i class="mdui-list-item-icon mdui-icon material-icons" style="color: #0041ff">book</i>
        <a href="/mdui-docs" target="_blank" class="mdui-list-item-content">MDUI文档</a>
    </li>
    <li class="mdui-list-item mdui-ripple">
        <i class="mdui-list-item-icon mdui-icon material-icons" style="color: #1abc9c">check_circle</i>
        <div class="mdui-list-item-content">质数检测</div>
        <div class="mdui-list-item mdui-textfield">
            <input id='input_number'class="mdui-textfield-input" placeholder="请输入要检验的数字" onchange="chk()">
        </div>
        <button class="mdui-btn mdui-btn-raised mdui-ripple" onclick="chk()">Check</button>
    </li>
    <li class="mdui-list-item mdui-ripple">
        <i class="mdui-list-item-icon mdui-icon material-icons" style="color: #66ccff">functions</i>
        <a href="https://webdemo.myscript.com/" target="_blank" class="mdui-list-item-content">在线识别手写公式</a>
    </li>
    <li class="mdui-list-item mdui-ripple">
        <i class="mdui-list-item-icon mdui-icon material-icons" style="color: #66ccff">location_searching</i>
        <a href="http://oeis.org/" target="_blank" class="mdui-list-item-content">数列找规律</a>
    </li>
</ul>