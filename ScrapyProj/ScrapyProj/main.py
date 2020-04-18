from scrapy.cmdline import execute
import sys
import os
 
# 用来设置工程目录，有了它才可以让命令行生效
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
 
# 用来获取当前py文件的路径
os.path.abspath(__file__)
# 用来获取文件的父亲的路径
os.path.dirname(__file__)    
 
# 调用execute()函数执行scarpy的命令 scary crawl 爬虫文件名字
execute(['scarpy','crawl','general'])