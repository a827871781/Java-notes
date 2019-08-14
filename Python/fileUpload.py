import sys
import requests

#python 学习的一个脚本
#上传图片 并 返回mackdown格式的字符串，并复制到剪切板
#用法
#1.图片保存至桌面
#2.命令行内进入桌面
#3.执行命令 python 脚本名 图片名  （要有后缀）

def main():
    fileName =  sys.argv[1]
    url = 'https://sm.ms/api/upload'
    file_obj=open('C:\\Users\\Administrator\\Desktop\\'+fileName,'rb')  
    files  = {'smfile':file_obj}
    r = requests.post(url, data=None, files=files)
    import json
    the_json = json.loads(r.text)
    mk = '![%s](%s )' % (fileName, the_json["data"]["url"])
    import pyperclip
    pyperclip.copy(mk)
    print("已复制")


if __name__ == "__main__":
    main()



