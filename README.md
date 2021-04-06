# dandanplay-resources-api

> 弹弹play下线资源搜索服务，提供了API规范，我现在打包的[网络上已实现的代码](https://pastebin.ubuntu.com/p/mGP7JRpBtd)，中国大陆需要提供http代理。

> 运行成功之后在弹弹play中配置如下：设置->网络与更新->自定义端点-> API端点地址留空，资源搜索节点 http://localhost:8000

## 动漫之家

### docker

```shell
# docker编译
docker build --build-arg MIRRORS=https://pypi.mirrors.ustc.edu.cn/simple -t dandanplay-resources/dmhy:1.0.0 dandanplay-resources/dmhy .
# docker运行
docker run -e DDP_HTTP_PROXY=http://192.168.1.54:1081 -e DDP_HOST=0.0.0.0 -e DDP_PORT=8000 -p 8000:8000 -d dandanplay-resources/dmhy
```
或者[下载](https://github.com/liaoheng/dandanplay-resources-api/releases/latest)导入镜像
```shell
#上传
 scp -P [端口] 本地镜像.tar.gz 用户名@服务器IP:服务器镜像路径
#导入
docker load -i 镜像.tar.gz
```


### 本地运行

```shell
#安装依赖
python -m pip3 install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple
#运行
python ddp_dmhy.py -x http://192.168.1.54:1081 -h 127.0.0.1 -p 8000
```
