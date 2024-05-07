# Kubernetes源码编译

## 下载与编译

- 为 WSL2 配置代理

```bash
host_ip=$(cat /etc/resolv.conf |grep "nameserver" |cut -f 2 -d " ")
export ALL_PROXY="http://$host_ip:7890"
```

- go 环境

```bash
# 1. go 环境
apt install build-essential make bison
snap install go --classic
bash <(curl -s -S -L https://raw.githubusercontent.com/moovweb/gvm/master/binscripts/gvm-installer)
gvm install go1.22.0
gvm use go1.22.0
```

- docker 

```bash
apt install build-essential
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh --mirror Aliyun
containerd config default > ~/config.toml
```

```toml
      [plugins."io.containerd.grpc.v1.cri".registry.mirrors]
        [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
          endpoint = ["https://hub-mirror.c.163.com","https://registry-1.docker.io"]
```

- 编译 rsync

```bash
apt install gcc g++ gawk autoconf automake python3-cmarkgfm acl libacl1-dev libzstd-dev liblz4-dev libssl-dev
```

- 克隆仓库

```bash
git clone https://github.com/kubernetes/kubernetes.git


sudo apt install build-essential
```
