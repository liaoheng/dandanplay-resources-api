# dandanplay-resources-api

```shell
#动漫之家
docker build --build-arg MIRRORS=https://pypi.mirrors.ustc.edu.cn/simple -t dandanplay-resources/dmhy:1.0.0 dandanplay-resources/dmhy .

docker run -e DDP_HTTP_PROXY=http://192.168.1.54:1081 -e DDP_HOST=0.0.0.0 -e DDP_PORT=8000 -p 8000:8000 -d dandanplay-resources/dmhy
```
