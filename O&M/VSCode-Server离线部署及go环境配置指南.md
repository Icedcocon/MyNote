# VSCode-Server离线部署及go环境配置指南

## 一、VSCode-Server内网迁移指南

- **只要一个用户配置好VSCode-Server，所有使用同一个VSCode安装包（即Commit ID相同）的用户都可以使用Remote-SSH插件直接连接，无需配置。**

- 压缩两个路径并迁移 
  
  - `/root/.vscode-server` 是VSCode的服务器以及插件
  
  - `/usr/local/go` 是go环境以及VSCode语法识别所需的二进制文件

```bash
cd /root
tar -czf vscode-server.tar.gz .vscode-server
scp vscode-server.tar.gz ${IP}:/root
ssh root@${IP} tar -xzf vscode-server.tar.gz

cd /usr/local/
tar -czf go.tar.gz go
scp go.tar.gz ${IP}:/usr/local
ssh root@${IP}:/usr/local tar -xzf go.tar.gz
```

- 随后即可尝试连接

## 二、VSCode-server配置go环境指南

### 1. go二进制文件下载

```bash
wget https://go.dev/dl/go1.22.3.linux-amd64.tar.gz
```

### 2. 解压并配置

```bash
# (1) 解压并移动
tar -xzf go1.22.3.linux-amd64.tar.gz
mv go /usr/local
# (2) 配置环境变量
echo 'export PATH=${PATH}:/usr/local/go/bin' >> /etc/profile
# (3) 重新进入shell
# (4) 配置环境变量（通常保持不变即可）
go env -w GOROOT='/usr/local/go' 
go env -w GOTOOLDIR='/usr/local/go/pkg/tool/linux_amd64'
```

### 3. 配置并迁移VSCode使用的go环境

- 使用VSCode连接当前节点的VScode-Server

- 首次连接时会提示下载格式化及语法高亮所需要的二进制文件，通常位于`${GOROOT}/bin` 下，如gofmt、gopls

- 如果下载失败可以配置代理为国内源

```bash
go env -w GOPROXY='https://goproxy.cn,direct'
```

- 下载完成后打包 `/usr/local/go` 并迁移至内网对应位置，然后配置 `/etc/profile` 中的 PATH 变量

- 在内网使用vscode连接服务器

## 三、VScode-Server离线部署说明

### 1. 安装包下载

- vscode

```bash
https://code.visualstudio.com/Download
```

- vscode-server

```bash
# For windows web
https://update.code.visualstudio.com/commit:提交的ID码/server-linux-x64/stable
# For Linux
curl -sSL "https://update.code.visualstudio.com/commit:提交的ID码/server-linux-x64/stable" -o vscode-server-linux-x64.tar.gz
```

- 插件
  
  - 在客户端中检索插件，进入插件详情页面，右侧 **Reousrces > Marketplace**
  
  - 进入Marketplace网页版后，右侧 **Reousrces > Download Extension**
  
  - PS： 也可以在外网部署好vscode-server后将 ~/.vscode-server 打包，其中会自动包含外网下载的插件，但是似乎多次迁移后插件有概率不可见，因此推荐首次迁移到内网时使用本方法节省时间。（PS的PS：本方案依然要替换掉~/.vscode-server/bin路径下的commit ID 路径，详见下文）

### 2. 内网部署

- 安装vscode客户端并安装Remote-SSH插件

- 在家目录创建以下**bin、extensions**路径结构，以root用户为例

```bash
.vscode-server
├── bin
└── extensions
```

- 将`vscode-server-linux-x64.tar.gz`放入`.vscode-server/bin`下解压并将解压后的文件夹重命名为commit ID
  - commit ID 可在 vscode 上方菜单栏的 **Help > About** 中查看

```bash
.vscode-server
├── bin
│   └── dc96b837cf6bb4af9cd736aa3af08cf8279f7685
└── extensions
```

- 使用vscode的remote-SSH插件连接vscode-server即可开始使用

## 
