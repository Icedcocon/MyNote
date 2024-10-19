# IPV6 隧道快速上手

## 一、说明

- 想要开启tailscale ipv6 P2P 连接，需要满足以下三个条件
  
  - (1) Derper 所在服务器具有 ipv6 公网地址
  
  - (2) 在 headscale 的配置文件中添加该 Derper 节点
  
  - (3) tailscale 客户端所在节点具有 ipv6 地址

## 参考资料

- Headscale IPV6 相关配置

[Headscale 部署和 DERP 服务器配置 - Phyng 的博客](https://phyng.com/2023/04/06/headscale.html)

- HE 隧道相关

https://www.bilibili.com/video/BV1nD421N7Qt/?spm_id_from=333.337.search-card.all.click&vd_source=fefc74ddfb7b0b365d1b1d4af922a0ba

[配置HE隧道服务获取无穷IPv6地址、内网穿透、外网访问 - 老E的博客](https://appscross.com/blog/how-to-configure-he-ipv6-tunnel.html)

- Derper IPV6 相关

[使用家庭宽带公网 IPV6 自建 Tailscale 的 DERP 节点](https://blog.hellowood.dev/posts/%E4%BD%BF%E7%94%A8%E5%AE%B6%E5%BA%AD%E5%AE%BD%E5%B8%A6%E5%85%AC%E7%BD%91-ipv6-%E8%87%AA%E5%BB%BA-tailscale-%E7%9A%84-derp-%E8%8A%82%E7%82%B9/)
