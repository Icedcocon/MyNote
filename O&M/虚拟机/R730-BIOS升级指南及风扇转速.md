# R730 BIOS升级指南及风扇转速

## 一、 iDRAC升级

### 1. 固件下载

- 登录DELL官网下载对应固件：  https://www.dell.com/support/home/zh-cn?app=products

- 下载后获取到文件 `iDRAC-with-Lifecycle-Controller_Firmware_WGNHP_WN64_2.82.82.82_A00_01.EXE`

### 2. 固件升级

- 点选iDRAC设置，更新和回滚。上传固件，并升级。

- 上载后，勾选，点击安装

- iDRAC升级不会重启服务器，因此直接点击安装。

- 因版本跨度过大，作业队列提示信息:
  
  - RED007: Unable to verify Update Package signature.

- 7z 解压 Update Package，上传 …/payload/firmimg.d7 进行更新。

- 等待iDRAC自动重启

> 注意：先升级iDRAC，再升级其他如BIOS等固件，可以避免出现签名等问题。

### 3. 故障修复

#### 3.1 出现 400 Bad Request 错误（有两种方法可以解决此问题）

ssh 连接 idrac 地址执行以下两种指令中的一种

- 1） 添加主机名

```bash
# 检查 ManualDNSEntry 是否为空
racadm get idrac.webserver
# 为空则设置 iDRAC hostname
racadm set idrac.webserver.ManualDNSEntry <hostname>
```

- 2） 禁用主机名检查

```bash
racadm set idrac.webserver.HostHeaderCheck 0
```

## 二、 BIOS升级

- 在 idrac 上传 `BIOS_HJ81K_WN64_2.14.0.EXE`

- 可以多上传几个固件后一起重新引导

## 三、风扇转速控制

## 参考资料

- 丁辉博客教程

https://www.dinghui.org/dell-idrac-upgrade.html

- R730 驱动下载地址

https://www.dell.com/support/home/en-mv/product-support/product/oth-r730/drivers

- 400 错误修复

[Data Domain: How to access the iDRAC v5.10.00.00 UI using hostname after upgrading DDOS | Dell US](https://www.dell.com/support/kbdoc/en-us/000210557/data-domain-idrac-gui-not-available-after-upgrade-of-ddos-400-bad-request-error)

- 风扇转速控制

https://www.dell.com/community/zh/conversations/poweredge%E6%9C%8D%E5%8A%A1%E5%99%A8/dell-r730-%E5%A2%9E%E5%8A%A0%E5%A4%96%E6%8E%A5%E6%98%BE%E5%8D%A1%E5%90%8E%E9%A3%8E%E6%89%87%E8%BD%AC%E9%80%9F%E5%BE%88%E5%A4%A7%E7%9A%84%E9%97%AE%E9%A2%98/647f7c2af4ccf8a8dea7b05a

https://www.dell.com/community/zh/conversations/poweredge%E6%9C%8D%E5%8A%A1%E5%99%A8/t630%E5%A1%94%E5%BC%8F%E6%9C%8D%E5%8A%A1%E5%99%A8%E5%8A%A0%E8%A3%85gpu%E5%99%AA%E9%9F%B3%E9%9D%9E%E5%B8%B8%E5%A4%A7/647f7915f4ccf8a8de72a9c1#M9648
