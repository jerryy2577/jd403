# jd403

频道: https://t.me/jd403ya
群组: https://t.me/jd403la
必看: [https://www.52hym666.top/](https://www.52hym666.top/)
上车: [京东短信车](https://jdc.52hym666.top/)
博客: [https://www.52hym666.top/](https://www.52hym666.top/archives/1111)
## 食用教程
1. 青龙面板拉库命令:  `ql repo https://github.com/jerryy2577/jd403.git "jd_|install_deps" "jd_farm" "utils|notify|db|conf|storage|jd_farm" "main"`
2. 青龙面板定时任务页面搜索:`install_deps`, 运行一次`一键初始化配置和安装依赖`任务。
3. 脚本管理找到`jerryy2577_jd403_main`文件中.env文件编辑, 根据注释提示修改配置。

## 自建服务
- jd sign:
```shell
docker run -d \
    --name=jd_sign \
    -p 32772:8080 \
    -v $PWD/jd_sign:/app/data \
    --restart=always \
    --log-opt max-file=2 \
    --log-opt max-size=50m \
    zhx47/jd_sign:latest
```
- jd h5st

```shell
docker run -d \
    --name jd_server \
    -p 3001:3001 \
    --log-opt max-file=2 \
    --log-opt max-size=50m \
    zhx47/jd_h5st_server:amd64
```

- 更新jd-sign/jd-h5st
```shell
 docker run --rm -v /var/run/docker.sock:/var/run/docker.sock containrrr/watchtower --cleanup -SR $(docker ps -a | grep 'zhx47/' | awk '{print $NF}')
```

## 其他说明

- 一对一推送支持青龙CK的备注格式为: `jerry@@1722410684021@@UID_iB2fdePmO6g`
