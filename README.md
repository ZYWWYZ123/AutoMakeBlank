# AutoMakeBlank 项目简介<br>
这个小玩意可以在英语文章中随机挖空。<br>
你可以用它来与你已有朗读音频的英语文章帮助你练习听力<br>
或者搞点其他的更有用的<br><br>

可能会在将来的版本改进必须下载某些第三方库才能使用程序的问题。毕竟不是每个人都需要那些功能<br>
我希望将它设计成需要某些功能就下载对应py文件而无需进行繁复设置的样子<br>

<h3>✔️这个程序可以干啥</h3>
<ul>
    <li>随机帮你给英语文章挖空，配合黑名单机制以避免在你不需要的地方挖空</li>
    <li>规范文章格式(目前还有些许格式错误存在，多与空格有关)</li>
    <li>不会重复挖空(‼️目前未解决相同单词的不同形式重复挖空-例如过去时/复数)</li>
</ul>
<h3>❌这个程序不可以干啥</h3>
<ul>
    <li>校对文章语法错误和单词拼写错误<br><br></li>
</ul>

# 关于 NetworkFunctions.py 【非必需文件】的使用说明<br>
## 从 1.1.0 版本开始正式引入了特定网站文本抓取。对该文件说明如下<br>
## 1.对于TED演讲稿抓取的说明：<br>
**适用版本：V1.1.0 ~ V1.1.3**<br>
**第三方库需求：selenium、lxml、bs4**<br>
**重要提示：需要安装Edge浏览器，需要安装Egde浏览器对应版本驱动** [->点击进入 Edge 驱动下载链接](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/#downloads "Edge驱动下载链接")<br>
将需要抓取的talk主页链接-*例如https://www.ted.com/talks/frances_s_chance_are_insect_brains_the_secret_to_great_ai*(可选：*/transcript*)链接粘贴到 article.txt 中。链接后不能包含例如rid=???或/comments等后缀。目前版本的程序没有添加识别这些内容的代码，也没有通过selenium库的点击来获取 (因为测试中出现了一些目前我无法解决的问题) ，仅通过获取元素来识别transcript部分。<br>
使用这个功能时**仅在txt文件中粘贴链接**即可，请勿加入其他文字造成干扰。<br><br>

## 2.对于CNN 10*字幕抓取的说明<br>
**适用版本：V1.1.2 ~ V1.1.3**<br>
**第三方库需求：requests**<br>
\*仅限于 http://www.listeningexpress.com/cnn10/ 站点中的文本抓取<br>
链接应类似于这样：http://www.listeningexpress.com/cnn10/2022-12-07%20Is%20The%20Economy%20Bad.html 才可被识别。这个网站的抓取依靠requests库完成，所以不需要打开额外的窗口。<br><br>

# 关于必需核心文件及非必须附加功能文件的说明<br>
**必需核心文件：**
<ul>
    <li>AutoBlankMaker(+版本号).py：此文件为主体文件</li>
    <li>TextFunctions.py：此功能提供挖空核心功能</li>
    <li>article.txt：此文件为程序读取文字所需文件</li>
</ul>

**非必需附加功能文件：**
<ul>
    <li>NetworkFunctions.py：提供网页抓取功能，具体见上，目前不可编辑</li>
    <li>wordBlkList.txt：提供单词黑名单功能，其中的单词不会被挖空</li>
    <li>wordWitList.txt：提供单词白名单功能，其中的单词被遍历到时一定会被挖去</li>
</ul><br>

## 关于文件使用方法的补充说明<br>
**如何运行程序**<br>
运行 AutoBlankMaker(+版本号).py 并按提示使用<br>

**TextFunctions.py**<br>
在本文件中的 ProgSetting 字典中包含了部分可编辑键值对(列在下方)：<br>
*程序检测到的单词数指输入文本的所有的单词数，包含已排除不挖空的单词*
<ul>
    <li>blankMinRate - 指挖空数量占程序检测到的单词数的最小比例</li>
    <li>blankMaxRate - 指挖空数量占程序检测到的单词数的最大比例</li>
    <li>blankRate - 指每次遍历单词列表时挖空的概率。在前面所有的检测(是否重复、是否在黑名单等)通过后才使用此概率决定是否挖空</li>
    <li>ignoreCapital - 指是否对首字母大写的单词挖空。True 为是，False 为否</li>
    <li>docxOutput - 【为将来版本做准备，目前没有用处】决定是否以 .docx 输出文本True 为是，False 为否</li>
</ul>
其余键值对不可编辑，否则会引起错误<br>

**wordBlkList.txt**<br>
此文件控制挖空黑名单。<br>
使用方法：以英文逗号间隔单词，或者以行间隔单词，二者皆可。例如：

---

apple,pear,fox,pineapple<br>
tomato,orange,strawberry,potato,cabbage,eggplant,carrot,watermelon-killer<br>

---

您应该注意到了：逗号间不能有空格，也没有短语出现，但可以有包含连字符的合成单词<br>
这个文件主要是让其中的单词不会被挖空。但一定注意，它无法预测单词的复数、过去时等形式。仅在完全匹配时才会规避。短语规避功能目前没有做出来<br>

**wordWitList.txt**<br>
此文件控制挖空白名单。其中的单词一定会被挖空。<br>
注意：白名单优先级最低，即低于已被挖去的单词、黑名单等。它的使用方法与黑名单一样。<br>

**article.txt**<br>
将你的文章或链接按使用方式粘贴在里面<br>

**@Test paper.txt 与 @Answer sheet.txt**<br>
@Test paper.txt 为挖完空后生成的文本文件，@Answer sheet.txt 为挖空处单词答案文件<br>

**其他生成的文件**<br>
这些文件为使用程序进行爬取时得到的的包含演讲稿/字幕等原内容的 txt 文件，可用于用户其他目的的使用。具体文件名取决于原标题<br><br>

# 关于测试中所用程序版本及第三方库的说明<br>
**根据我电脑中程序版本列出，仅保证以下版本程序的正确运行**<br>
1.此程序在python版本 3.9.2, 64-bit 下测试<br>
2.所用第三方库版本(从 bs4 导入子库 beautifulsoup)：<br>
beautifulsoup4==4.11.1<br>
bs4==0.0.1<br>
lxml==4.9.2<br>
requests==2.28.1<br>
selenium==4.7.2<br><br>

# Version 1.1.3更新内容<br>
1.修复了某些横线会意外的长的问题<br>
2.为网页爬取功能增加试错机制，在失败5秒后会重新尝试爬取或加载网页<br>
3.修复了 CNN 字幕无法正确去除的问题。现在，所有检测到标记的字幕会被统一输出为【SUBTITLE】标识并去除内容文本<br>
4.修复了某些情况下对标记为 CNN 的文章挖空时名字部分标识不正确的问题<br>

# Version 1.1.2更新内容<br>
1.增加CNN演讲稿(目前**仅限于第三方网址** *http://www.listeningexpress.com/cnn10/* )TXT文本抓取<br>
2.从该版本开始，你可以不必下载全部的文件(当你不需要某些功能时)，只需要下载核心文件即可。具体说明见上方<br>
3.对程序提示文本进行了重写，在 TextFunctions.py 的字典 ProgSetting 中增加一个可选功能<br>
4.引入白名单功能，此功能可以让其中的单词一定被挖空(当程序遍历到这个位置)<br>
5.小部分程序结构改进<br>

# version 1.1.1更新内容<br>
1.更正了某些格式上和程序上的错误<br>
2.修复了因TED演讲题目含有非法符号造成写入文件失败的问题<br>
3.程序优化，减少一些处理压力，删除不必要部分<br>

# Version 1.1.0更新内容<br>
1.V1.1.0 版本已经上载。此版本增加了抓取TED Transcript的功能。需要将链接（1个）粘贴到article.txt中<br>
2.注意：链接形如：https://?????/talks/?????to_yourself，即不能以"rid=??????"结尾<br>
3.上述以"rid=??"结尾的链接将在下个版本中增加支持<br>
4.此外，该版本改进了一些程序逻辑及删除了一些无用代码<br>
5.下一版本将着重于程序性能改进及错误修复<br>
