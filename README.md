原项目地址
https://github.com/qicfan/q115-strm

docker build后的镜像有问题，只能用原镜像qicfan/115strm:latest建container，copy修改过的文件到container中：
frontend/assets/index-yGtPj0fc.js
frontend/cookie.html
job.py
lib.py
life_event_change.py
get_cookie.py
server.py

生成新的镜像
docker commit q115-strm my-q115-strm:latest
docker commit my-q115-strm my-q115-strm:latest

用新镜像建container
    docker-compose.yml
    services:
      115strm:
        image: my-q115-strm:latest
        container_name: my-q115-strm
        environment:
          - TZ=Asia/Shanghai
          - replace_cd2_with_alist=True
        ports:
          - target: 12123
            published: 12123
            protocol: tcp
        volumes:
          - /vol1/1000:/vol1/1000 #映射clouddrive所在路径
          - /vol1/1000/docker/my-q115-strm/data:/app/data # 运行日志和数据
          - /vol1/1000/strm:/media # 存放STRM文件的根目录
    
        restart: unless-stopped


新建115账号
    通过命令行扫码获取cookie，以下脚本在windows下也可以执行
    windows下命令(生成图片)
        python3 /app/get_cookie.py wechatmini -o
    linux下命令(直接在终端打印二维码)
        python3 /app/get_cookie.py wechatmini
    或者网页扫码
        http://192.168.3.102:12123/cookie
新建同步配置
    用cd2方式生成本地路径时能选择复制元数据，复制字幕文件，但cd2路径起播速度较慢
    replace_cd2_with_alist True 替换路径为alist的路径
    此参数应该在任务页面能配置，但并没有实现，现在默认为True

    对iso类型的视频单独配置
    replace_cd2_with_local 是否替换路径为本地路径
    local_path 本地路径(coreelec或芝杜挂载的cd2路径， 也可以用本地smb或nsf路径) 默认: /storage/videos/CloudNAS/CloudDrive/115

修改data/config/cron.tab并上传到container映射的目录，定时判断115有没有增删改事件，如果有则同步增删改strm
-k 参数为同步配置的key，查看/vol1/1000/docker/my-q115-strm/data/config/libs.json获取

增加emby_pinyin.py
https://github.com/whorace97/emby_pinyin

Emby拼音首字母搜索和按拼音排序，通过修改nfo文件达到效果，仅会处理电影与电视剧的nfo文件，不处理季、集的文件，程序将修改nfo文件中的originaltitle和sorttitle两个字段，并且会备份原有信息，修改后可以实现用拼音首字母搜索、按照拼音首字母排序的效果。
通过传入--restore指令可以恢复程序对nfo文件做出的修改。如果只想看一下程序将如何对你的文件进行处理，可传入--dry-run或者-n。程序对你的文件做出的修改将以html格式保存在 ./diff 文件夹中，可通过--diff-out指定文件夹。
程序使用自动化xml生成程序，可能会将原文件中不规范的的 双引号 替换为 " ，这不是程序错误哦。

python emby_pinyin.py -d '文件夹'

修改data/config/cron.tab, 增加定时更新nfo文件，并上传到container映射的目录
0 10 * * * python3 /app/emby_pinyin.py -d /media

