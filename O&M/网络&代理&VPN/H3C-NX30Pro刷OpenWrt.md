# H3C-NX30Pro 刷 OpenWrt

- 复制备份文件

```bash
scp -O  -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedAlgorithms=+ssh-rsa ./uboot.bin  H3C@192.168.124.1:/tmp
```

## 参考资料

- 酱紫表

[H3C NX30Pro 刷 openwrt 教程](https://blog.qust.me/nx30pro)

- 刷官方镜像

https://ericclose.github.io/install-openwrt-on-h3c_magic-nx30-pro.html


