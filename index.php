<?php
// 遍历文件夹
function each_path($dir) 
{
    $mods_json = array();
    if($handle = opendir($dir)) //注意这里要加一个@，不然会有warning错误提示：）
    { 
        while(($file = readdir($handle)) != false) 
        {
            if($file != ".." && $file != ".") 
            { 
                //排除根目录；
                if(is_dir($dir."/".$file)) 
                { 
                    //如果是子文件夹，就进行递归
                    $mods_json = array_merge($mods_json, each_path($dir."/".$file));
                } 
                else if($file != ".DS_Store")
                { 
                    //不然就将文件的名字存入数组
                    $mod_info = array(
                        "文件名" => $file,
                        "file_md5" => md5_file($dir."/".$file), // md5和python不同，暂时弃用
                        "file_name_md5" => md5($file)
                    );
                    array_push($mods_json, $mod_info);
                }
            }
        }
        closedir($handle);
        return $mods_json;
    }
}
// echo "<pre>";
$mods_info_json = file_get_contents("./server.json");
echo($mods_info_json);
// echo "</pre>";
?>