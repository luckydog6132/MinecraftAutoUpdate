#coding:utf-8
import os;
import os.path;
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
#----------------------------↑↑↑↑↑↑↑↑↑↑↑↑↑ 通用方法 ↑↑↑↑↑↑↑↑↑↑↑↑↑----------------------------
if __name__ == "__main__":
    # 配置文件
    _config_file_path = "./update.cfg"
    cfg = ConfigParser.ConfigParser()
    cfg.read(_config_file_path)
    # 读取配置
    _minecraft_path = cfg.get('File Path', 'minecraft');
    _minecraft_mods_path = cfg.get('File Path', 'minecraft_mods');
    _update_mode = cfg.get('Update Info', 'update_mode');

    # 文件是否存在
    if os.access(_minecraft_path, os.F_OK) and os.access(_minecraft_mods_path, os.F_OK):
        print ".minecraft and mods exits";
    else:
        print "文件错误";
        exit(0);

    # Offline 模式
    if _update_mode == "Online":
        print "Online";
        # download_file_save_to_path("http://127.0.0.1/forpython/[测试用jar包].jar","./[测试].jar");
    else:
        # Offline
        print "Offline";
        _update_file_path = cfg.get('Offline Update Info', 'update_file');
        # 文件中的字典内容
        update_json = [];
        with open(_update_file_path) as load_file:
            update_dict = load_file.read()
            load_file.close;
            update_json = json.loads(update_dict);

        # 遍历更新信息，查看是否有对应本地文件
        for info_dic in update_json:
            if is_exits_file(info_dic, _minecraft_mods_path) == False:
                print "缺少文件:" + info_dic["file_name"].encode("utf-8")
    