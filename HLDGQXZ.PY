# -*- coding: UTF-8 -*-
import urllib.request, re
import colorama, os, hashlib
os.system("CLS")
colorama.init(autoreset=True)
 
def md5(x):
    return hashlib.md5(x.encode(encoding='UTF-8')).hexdigest()
def getHtml(url):
    html = urllib.request.urlopen(url).read()
    return html
 
def saveHtml(file_name, file_content, filetype="html"):
    with open("%s.%s"%(file_name, filetype), "wb") as f:
        f.write(file_content)

def getSongsList():
    songsurllist=["http://www.hldbtv.com/ProgramsData/Channel_804/Index.aspx",
             "http://www.hldbtv.com/ProgramsData/Channel_804/Index_2.aspx",
             "http://www.hldbtv.com/ProgramsData/Channel_804/Index_3.aspx",
             "http://www.hldbtv.com/ProgramsData/Channel_804/Index_4.aspx",
             "http://www.hldbtv.com/ProgramsData/Channel_804/Index_5.aspx"]
    a=0
    for i in songsurllist:
        saveHtml("l%d"%a, getHtml(i))
        a+=1
def getSongsInfo():
    songslist=[]
    for i in range(5):
        with open("./l%d.html"%i, "r", encoding="u8") as f:
            """<a href="/ProgramsData/Item_137670.aspx" target="_blank">
                <img src="/UploadFiles/ztlm/2020/12/202012171109570996.jpg"
                alt="NO.XXX xxx" width="365" height="93" border="0">
            </a>"""
            for i in re.findall("<dd>([\\s\\S]*?)</dd>", f.read()):
                songslist.append(
                    {
                        "title": re.search("(NO.*?)\\\"", i).group(1),
                        "url": re.search("href=\\\"(.*?)\\\"", i).group(1)
                    }
                )
    return songslist
#getSongsInfo()
def downloadSongPage():
    j=0
    for i in getSongsInfo():
        print(i["url"])
        print(i["title"])
        saveHtml("./PAGES/s%d"%j, getHtml("http://www.hldbtv.com%s"%i["url"]))
        j+=1
#downloadSongPage()
def handleImg(md):
    imgsrc=md.group(1)
    imgsrcStored=md5(imgsrc)
    imgType=md.group(2)
    #http://www.hldbtv.com/UploadFiles/ztlm/2020/12/202012032136155606.jpg
    print("\033[5;37;42m%s\033[0m->%s"%(imgsrc, imgsrcStored))
    if False:
        with open("./PAGES/IMG/%s.%s"%(imgsrcStored, imgType), "wb") as f:
            f.write(getHtml("http://www.hldbtv.com%s.%s"%(imgsrc, imgType)))
    return "src=\"../IMG/%s.%s\""%(imgsrcStored, imgType)
def getSong():
    j=0
    for i in getSongsInfo():
        with open("./PAGES/s%d.html"%j, "r", encoding="u8") as f:
            htm=f.read()
            try:
                musicSrc=re.search(
                    "src=\\\"(http://audio.hldbtv.com/ProgramVOD/.*?)(mp3|wav)\\\".*?></audio>",
                    htm
                )
                musicType=musicSrc.group(2)
                musicSrc=musicSrc.group(1)+musicType
                print("\033[5;37;44m%s\033[0m"%i["title"])
                print("\033[5;37;44m%s\033[0m"%musicSrc)
                outline=re.search("id=\\\"content\\\">([\\s\\S]*?)<div class=\\\"domMobile\\\">", htm).group(1)
                outline=re.sub("<audio.*?</audio>", "", outline)
                outline=re.sub("src=\\\"(.*?)\\.(jpg|gif|png)\\\"", handleImg, outline)
                outline=re.sub("\\s*?</div>\\s*?</div>\\s*?</div>", "", outline)
                outline=re.sub("(^\\s*|\\s*$)", "", outline)
                imglst =re.findall("src=\\\"(.*?)\\.(jpg|gif|png)", outline)
                outline=re.sub("</*(span|p|strong|source|img)+.*?/*>", "", outline)
                imglst=list(map(lambda x: "<img src=\"%s.%s\">"%(x[0], x[1]), imglst))
                if not "br" in outline:
                    outline=outline.replace("\n", "<br />")
                outline=\
"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
	<meta charset="UTF-8">
    <link rel="stylesheet" href="./main.css">
	<title>%s</title>
</head>
<body>
	<div id="gc">
        %s
        <div style="clear: both"></div>
    </div>
    <div id="tp">
        %s
        <div style="clear: both"></div>
    </div>
    <div id="bt">
        %s
    </div>
    <div id="xx">
        主办：中共葫芦岛市委宣传部 <br />
        承办：葫芦岛传媒集团 <br />
        协办：辽宁兴达实业集团 <br />
        更多消息请参阅原网站：<a href="http://www.hldbtv.com/ProgramsData/Channel_804/Index.aspx">http://www.hldbtv.com/ProgramsData/Channel_804/Index.aspx</a>
    </div>
</body>
</html>
"""%(i["title"], outline, "".join(imglst), i["title"])
                print("\033[5;30;44m[\033[0m\033[5;30;43m%s\033[0m\033[5;30;44m]\033[0m"%outline)
                if False:
                    with open("./PAGES/MUS/%d.%s"%(j, musicType), "wb") as f:
                        f.write(getHtml(musicSrc))
                if not True:
                    with open("./PAGES/PGE/%d.htm"%j, "wb") as f:
                        f.write(outline.encode("u8"))
                if not True:
                    os.system("start chrome --enable-logging --headless --disable-gpu --screenshot=%s\\PAGES\\PIC\\%d.png --hide-scrollbars --window-size=1920,1080 %s\\PAGES\\PGE\\%d.htm"%(os.getcwd(), j, os.getcwd(), j))
                if not True:
                    os.system(".\\FFMPEG\\bin\\ffmpeg -r 15 -f image2 -loop 1 -i %s\\PAGES\\PIC\\%d.png -i %s\\PAGES\\MUS\\%d.mp3 -s 1920x1080 -pix_fmt yuvj420p -shortest -vcodec libx264 %s\\PAGES\\VID\\%d.mp4"%(os.getcwd(), j, os.getcwd(), j, os.getcwd(), j))
                if True:
                    os.system("REN .\\PAGES\\VID\\%s.mp4 %s.mp4"%(j, "%s%s"%("{:0>3d}".format(j+1), i["title"].split("《")[1][0:-1])))
            except Exception as e:
                print("\033[5;37;44mERROR\033[0m:\r\n\t%s\r\n\033[5;37;44mAT\033[0m:\r\n\t s%s.html\r\n"%(str(e), j))
        j+=1
getSong()
