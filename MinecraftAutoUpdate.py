#coding:utf-8
import os;
import os.path;
import urllib;
import requests;
import hashlib;
import ConfigParser;
import json;
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
# 查看本地是否有文件
def is_exits_file(file_json, mods_path):
    for parent,dirnames,filenames in os.walk(mods_path):    
        for filename in filenames:
            cur_file_md5 = get_file_md5(os.path.join(parent,filename))
            if cur_file_md5 == file_json["file_md5"]:
                # print "存在文件" + info_dic["file_name"].encode("utf-8");
                return True;
    return False;
# 删除本地文件
def remove_exits_file(file_md5, mods_path):
    for parent,dirnames,filenames in os.walk(mods_path):    
        for filename in filenames:
            cur_file_md5 = get_file_md5(os.path.join(parent,filename))
            if cur_file_md5 == file_md5:
                print "delete : "+file_md5;
                os.remove(os.path.join(parent,filename));
# 获取更新信息
def get_update_json_info(cfg):
    _update_mode = cfg.get('Update Info', 'update_mode');
    # Offline 模式
    # 接口获取内容或离线内容
    update_json = [];
    if _update_mode == "Online":
        # Online
        print "Online";
        _server_request = cfg.get('Online Update Info', 'server_request');
        
        # 获取接口信息
        response = requests.get(_server_request);
        if response.status_code == 200:
            update_json = json.loads(response.content);
        else :
            print "http error code:" + response.status_code;
    else:
        # Offline
        print "Offline";
        _update_file_path = cfg.get('Offline Update Info', 'update_file');

        # 文件中的字典内容
        with open(_update_file_path) as load_file:
            update_dict = load_file.read()
            load_file.close;
            update_json = json.loads(update_dict);
    return update_json;
#----------------------------↑↑↑↑↑↑↑↑↑↑↑↑↑ 通用方法 ↑↑↑↑↑↑↑↑↑↑↑↑↑----------------------------
if __name__ == "__main__":
    # 配置文件
    _config_file_path = "./update.cfg"
    cfg = ConfigParser.ConfigParser()
    cfg.read(_config_file_path)
    # 读取配置
    _minecraft_path = cfg.get('File Path', 'minecraft');
    _minecraft_mods_path = cfg.get('File Path', 'minecraft_mods');
    _update_download_url = cfg.get('Update Info', 'update_download_url');
    
    # 文件是否存在
    if os.access(_minecraft_path, os.F_OK) and os.access(_minecraft_mods_path, os.F_OK):
        print ".minecraft and mods exits";
    else:
        print "config file error";
        exit(0);

    # 根据在线模式或者离线模式获取内容后，进行更新
    update_json = get_update_json_info(cfg);

    # 遍历更新信息，查看是否有对应本地文件
    for info_dic in update_json["mods_list"]:
        if is_exits_file(info_dic, _minecraft_mods_path) == False:
            print "缺少文件:" + info_dic["file_name"].encode("utf-8");
            download_file_save_to_path(_update_download_url+info_dic["file_name"].encode("utf-8"),_minecraft_mods_path+info_dic["file_name"].encode("utf-8"));
    # 删除指定文件
    for delete_md5 in update_json["delete_mod"]:
        remove_exits_file(delete_md5,_minecraft_mods_path);
            
            