docker build后的镜像有问题，只能用原镜像建container，copy修改过的文件到container中：
frontend/assets/index-yGtPj0fc.js
job.py
lib.py
life_event_change.py
get_cookie.py

生成新的镜像
docker commit q115-strm my-q115-strm:latest

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
    python3 /app/get_cookie.py wechatmini -o
新建同步配置
    用cd2方式生成本地路径时能选择复制元数据，复制字幕文件，但cd2路径起播速度较慢
    replace_cd2_with_alist True 替换路径为alist的路径
    此参数应该在任务页面能配置，但并没有实现，现在默认为True

修改data/config/cron.tab并上传到container映射的目录，定时判断115有没有增删改事件，
如果有同步增删改strm
-k 参数为同步配置的key

