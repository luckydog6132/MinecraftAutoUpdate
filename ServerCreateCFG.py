#coding:utf-8
import os;
import os.path;
import hashlib;
import ConfigParser;
import json;
import sys;
import urllib;
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
    if the_request:
        with open(savePath, "wb") as save_data:
            save_data.write(the_request.content)
#----------------------------↑↑↑↑↑↑↑↑↑↑↑↑↑ 通用方法 ↑↑↑↑↑↑↑↑↑↑↑↑↑----------------------------
if __name__ == "__main__":
    # 配置文件
    _config_file_path = "./Server.cfg"
    cfg = ConfigParser.ConfigParser()
    cfg.read(_config_file_path)
    # 读取配置
    _server_mods_path = cfg.get('Server Info', 'server_mods');
    _save_file = cfg.get('Server Info', 'save_file');

    # 保存的内容
    server_mod_info = [];

    # 遍历mods文件
    for parent,dirnames,filenames in os.walk(_server_mods_path):    
        for filename in filenames:
            # print os.path.join(parent,filename) + "===" + get_string_md5(filename) + "===" + get_file_md5(os.path.join(parent,filename));
            # jar文件才保存
            if ".jar" in filename:
                file_info_dict = {
                    "file_name" : filename,
                    "file_name_md5" : get_string_md5(filename),
                    "file_md5" : get_file_md5(os.path.join(parent,filename))
                }
                server_mod_info.append(file_info_dict)

    # 保存到文件
    with open(_save_file, 'w') as file:
        file.write(json.dumps(server_mod_info, indent=2, ensure_ascii=False)) # 支持中文