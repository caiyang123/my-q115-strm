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

