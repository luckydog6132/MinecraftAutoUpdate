#coding:utf-8
import os;
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
#----------------------------↑↑↑↑↑↑↑↑↑↑↑↑↑ 通用方法 ↑↑↑↑↑↑↑↑↑↑↑↑↑----------------------------
# 配置文件
_config_file_path = "./update.cfg"
cfg = ConfigParser.ConfigParser()
cfg.read(_config_file_path)

# 读取配置
_minecraft_path = cfg.get('File Path', 'minecraft');
_minecraft_mods_path = _minecraft_path + "/mods";

# 文件是否存在
if os.access(_minecraft_path, os.F_OK) and os.access(_minecraft_mods_path, os.F_OK):
    print ".mine and mods exits";
else:
    print "文件错误";
    exit(0);

# 遍历mods文件
list = os.listdir(_minecraft_mods_path) 
#列出文件夹下所有的目录与文件
for i in range(0,len(list)):
    path = os.path.join(_minecraft_mods_path,list[i])
    if os.path.isfile(path):
        md5val = get_file_md5(path);
        print list[i] + "====" +md5val;