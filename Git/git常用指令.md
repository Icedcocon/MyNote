```bash
# fork公司/开源项目的代码仓库  ==》 得到 个人远端仓库
git fork https://github.com/${Co.}/${repo}.git（主仓库的URL）
# 将个人远端仓库clone到本地服务器  ==》 得到 本地代码仓库
git clone git@github.com:${Own}/${repo}.git(个人仓库URL)
# 进入项目路径下(该目录下有.git目录) ==》 设置 用于拉取和上传的远端仓库地址
git remote add upstream https://github.com/${Co.}/${repo}.git（主仓库的URL）
# 禁止 向远端主仓库进行代码提交
git remote set-url --push upstream no_push
# 查看 本地关联的代码库
git remote -v
# checkout  ==》 切换 开发分支
git checkout ${origin/RemoteBranch}
# 在${Branch}分支上建立自己的分支
git checkout -b ${LocalBranch}
# 查看当前分支
git branch
# 开发
*****************

# 查看那些文件修改了
git status
# 提交好修改的文件大本地仓库
git add filename1 filename2
# 提交commit 信息（代码提交的检索信息 符合公司开发规范）
git commit --amend (git commit -m "公司的规范")
# 推送到本地同时提交PR
git push -f origin ${LocalBranch}(本地分支):${RemoteBranch}(远端分支)
```

```bash
# 拉取远端仓库代码（在本地建立与远端的仓库的分支同时取名为分支名）
git fetch upstram
git fetch upstram ${RemoteBranch}(远端分支):${LocalBranch}(本地分支)
# 进行合并操作(可以使用rebase 和merege两种操作)
# 在本地项目路径下 将${LocalBranch}(最新的)合并到master分支(当前本地分支)
git checkout master
git rebase ${LocalBranch}(本地分支) 
git merge ${LocalBranch}(本地分支) 

# 出现conflict问题
*****************************
# 查看有哪些文件有冲突
git diff
# 解决冲突
******************************
# 重新提交刚刚解决冲突的文件
git add filename1 filename2
# 提交commit 信息（代码提交的检索信息 符合公司开发规范）
git commit --amend
# 推送到本地同时提交PR 
git push -f origin ${LocalBranch}(本地分支):${RemoteBranch}（远端分支）
```

```bash
# 查看历史commit id及信息
git log
# 版本回退并丢弃后面的修改内容
git reset --hard ${commitID}
# 因为版本比origin更旧因此需要使用push -f强制更新
git push -f origin ${LocalBranch}(本地分支):${RemoteBranch}（远端分支）
# 版本回退并保留之后的修改
git revert -n ${commitID}
# 提交commit 信息（代码提交的检索信息 符合公司开发规范）
git commit --amend
# 推送到本地同时提交PR 
git push origin ${LocalBranch}(本地分支):${RemoteBranch}（远端分支）
```

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

```bash
# 切换到A分支
git checkout A
# 获取A分支最新代码
git pull
# 切换到B分支
git checkout B
# 获取B分支最新代码
git pull
# 合并分支
git merge A

# 切换到A分支
git checkout A
# 获取A分支最新代码
git pull
# 切换到B分支
git checkout B
# 获取B分支最新代码
git pull
# 合并指定文件或者文件夹到分支
git checkout A README.md

# git已跟踪且修改 并忽略改文件
# (1) 忽略单个文件：
git update-index --assume-unchanged sessions/abc.xml
# (2) 忽略多个文件：
git update-index --assume-unchanged sessions/*.xml
# (3) 忽略文件夹：
git update-index --assume-unchanged sessions/
```

```bash
# 机器A
# 创建git代码仓库
git init
git config --global --add safe.directory /<path>/project
git add .
# git branch -m master
# git config --global user.name "Your Name"
# git config --global user.email you@example.com
git commit -m "create project"

# 切换到project父目录，创建一个project-bare目录
cd ..
mkdir project-bare
cd project-bare

# 从原始代码仓库创建bare仓库，作为“中央”仓库，其他机器(包括本机的原始仓库)往这里push，从这里pull
git clone --bare ../project ./project-bare.git

# 回到project仓库目录
cd ../project

# 把project-bare添加为remote，
git remote add origin ../project-bare/project-bare.git
git branch --set-upstream-to=origin/master master


# 机器B
git clone ssh://<username>@<ip>:/codes/project-bare/project-bare.git ./project
```
