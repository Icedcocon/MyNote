```bash
# 查看全局配置
git config --global --list     #文件不存在时，可以任意设置一个全局配置生成文件

# git本地个人信息配置
git config --global user.email "your email"
git config --global user.name "your name"

# 换行符设置
git config --global core.autocrlf true # push时自动转换crlf为lf，pull 时相反
git config --global core.safecrlf true # 不允许提交含不同换行符的文件

# 字符集设置(解决中文乱码)
git config --global core.quotepath false # 显示 status 编码
git config --global gui.encoding utf-8   # 图形界面编码
git config --global i18n.commit.encoding utf-8   # 处理提交信息编码
git config --global i18n.logoutputencoding utf-8 # 输出 log 编码
export LESSCHARSET=utf-8  # 因为 git log 默认使用 less 分页，所以需要 bash 对 less 命令处理时使用 utf-8 编码

# 常用指令
touch README.md    # 提交文件
git init
git add README.md    # git add . 添加所有文件
git commit -m "init commit"
git remote add origin http://XXXXXX:11000/GogsAdmin/demo-server.git # 添加并推送已创建的仓库至远程仓库
git push -u origin master
```
