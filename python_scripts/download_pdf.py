from concurrent.futures import ThreadPoolExecutor
import requests,argparse,re,os
from bs4 import BeautifulSoup

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'
    }
    
## 设置命令行参数
def setArgs():
    parser = argparse.ArgumentParser(description="功能：下载pdf")
    parser.add_argument("url",help="目标url")
    parser.add_argument("-t","--thread",help="最大的线程数。默认为3",default=3,type=int)
    parser.add_argument("-f","--filedir",help="文件保存的路径.默认为当前目录下的downloads文件夹.如果不存在，便自动新建",default="downloads")
    return parser.parse_args()
    
## 获取所有pdf的url
def getPdfUrl(root_url):
    response = requests.get(root_url, headers=headers)
    ## 如果requests没有从页面中获得字符编码，那么设置为utf-8
    if "charset" not in response.headers:
        response.encoding = "utf-8"
    bsObj = BeautifulSoup(response.text, "html.parser")
    pdfs = bsObj.find_all("a", {"href": re.compile(r'.pdf$')})
    ## 获得一个字典，key为pdf完整url，value为pdf名称
    url_pdfName = {pdf['href']:pdf['href'].strip().split('/')[-1] for pdf in pdfs}
    return url_pdfName

## 显示正在下载的pdf的名称
def showPdf(pdf_name):
    print(pdf_name+"...")

## 下载pdf
def savePdf(url,pdf_name):
    response = requests.get(url,headers=headers,stream=True)
    ## 如果指定的文件夹，那么便新建
    if not os.path.exists(FILE_DIR):
        os.makedirs(FILE_DIR)
    ## os.path.join(a,b..)如果a字符串没有以/结尾，那么自动加上\\。（windows下）
    with open(os.path.join(FILE_DIR,pdf_name),"wb") as pdf_file:
        for content in response.iter_content():
            pdf_file.write(content)

## 设置要下载一个pdf要做的事情，作为线程的基本
def downOne(url,pdf_name):
    showPdf(pdf_name)
    savePdf(url,pdf_name)
    print(pdf_name+" has been downloaded!!")
    
## 开始线程
def downPdf(root_url,max_thread):
    url_pdfName = getPdfUrl(root_url)
    with ThreadPoolExecutor(max_thread) as executor:
        executor.map(downOne,url_pdfName.keys(),url_pdfName.values())

def main():
    ## 获得参数
    args = setArgs()
    ## 如果没有输入必须的参数，便结束，返回简略帮助
    try:
        global FILE_DIR
        FILE_DIR = args.filedir
        downPdf(args.url,args.thread)
    except:
        exit()

if __name__ == "__main__":
    raw_url = 'http://clinicalmetagenomics.org/iccmg-2016/'
    main()

