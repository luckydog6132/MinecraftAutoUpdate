#coding:utf-8
import os;
import os.path;
import requests;
import hashlib;
import ConfigParser;
#----------------------------↓↓↓↓↓↓↓↓↓↓↓↓↓ 通用方法 ↓↓↓↓↓↓↓↓↓↓↓↓↓----------------------------
# 计算文件md5
def get_file_md5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
        f.close()
        return myhash.hexdigest()
# 字符串MD5
def get_string_md5(inputString):
    md5String = hashlib.md5()   
    md5String.update(inputString)   
    return md5String.hexdigest()
# 下载文件, 并保存
def download_file_save_to_path(urlString, savePath):
    the_request = requests.get(urlString) 
    with open(savePath, "wb") as save_data:
        save_data.write(the_request.content)
#----------------------------↑↑↑↑↑↑↑↑↑↑↑↑↑ 通用方法 ↑↑↑↑↑↑↑↑↑↑↑↑↑----------------------------
# 配置文件
_config_file_path = "./update.cfg"
cfg = ConfigParser.ConfigParser()
cfg.read(_config_file_path)

# 读取配置
_minecraft_path = cfg.get('File Path', 'minecraft');
_minecraft_mods_path = cfg.get('File Path', 'minecraft_mods');

# 文件是否存在
if os.access(_minecraft_path, os.F_OK) and os.access(_minecraft_mods_path, os.F_OK):
    print ".minecraft and mods exits";
else:
    print "文件错误";
    exit(0);

# #遍历mods文件
# for parent,dirnames,filenames in os.walk(_minecraft_mods_path):    
#     for filename in filenames:
#         # print filename + "===" + get_file_md5(os.path.join(parent,filename));
#         print filename + "===" + get_string_md5(filename);

download_file_save_to_path("http://127.0.0.1/forpython/[测试用jar包].jar","./[测试].jar");