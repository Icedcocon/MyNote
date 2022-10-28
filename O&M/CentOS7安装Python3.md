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
