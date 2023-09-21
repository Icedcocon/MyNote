## CentOS 7: 安装Python3

```bash
# 下载依赖
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel \
sqlite-devel readline-devel tk-devel gdbm-devel db4-devel \
libpcap-devel xz-devel gcc
yum -y install epel-release libffi-devel python-pip
# 下载源码
wget https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tar.xz

# 解压并安装
tar -xf Python-3.9.9.tar.xz
cd Python-3.9.9
./configure prefix=/usr/local/python3 --with-ssl
make && make install

# 添加链接
ln -s /usr/local/python3/bin/python3.9 /usr/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
```

## CentOS 8: yum设置为源

发布于 2022-02-25 13:56:49

3.4K1

举报

1、将源文件备份

```javascript
cd /etc/yum.repos.d/ && mkdir backup && mv *repo backup/
```

复制

2、下载源文件

```javascript
curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-8.repo
```

复制

3、更新源里面的地址

```javascript
sed -i -e "s|mirrors.cloud.aliyuncs.com|mirrors.aliyun.com|g " /etc/yum.repos.d/CentOS-*
sed -i -e "s|releasever|releasever-stream|g" /etc/yum.repos.d/CentOS-*
```

复制

4、生成缓存

```javascript
yum clean all && yum makecache
```
