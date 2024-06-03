# Tradextr

## 环境初始化 (Required)

1. 终端中执行`./script/init.sh` 或者 VSCode 中使用快捷键`Ctrl` + `Shift` + `B`

## 临时调试

1. 修改./src/test.py 中的内容(不用提交到 git)
2. 终端中执行`./script/test.sh` 或者 VSCode 中使用快捷键`Ctrl` + `Shift` + `T`

## 部署运行 API Server

> 为节省磁盘空间, 使用目录绑定避免重复安装依赖

### 开发环境

> .env 中添加 SERVER_RELOAD=true 开启文件修改自动 reload

```shell
# 启动
docker compose up
# 停止
# Ctrl + C
```

### 正式环境

> 后台运行 && 开机自启动

```shell
# 启动
docker compose up -d

# 停止
docker compose down
```
