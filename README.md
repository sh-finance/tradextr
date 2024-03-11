# Tradextr

## 环境初始化

```shell
./script/init.sh
```

## 开发环境

1. 复制`.env.template`到`.env`，修改其中的环境变量
2. `./script/dev.sh` 启动开发环境，默认开启 reload, 可以通过环境变量`RELOAD=False`覆盖

## 部署

1. 安装 pm2
2. 复制`.env.template`到`.env`，修改其中的环境变量
3. `pm2 start|restart|stop ecosystem.config.js`

## 开机自启动

```shell
pm2 save
pm2 startup
```

## 临时调试

1. 修改./src/test.py 中的内容(不用提交到 git)
2. 终端中执行`./script/test.sh` 或者 VSCode 中使用快捷键`Ctrl` + `Shift` + `B`
