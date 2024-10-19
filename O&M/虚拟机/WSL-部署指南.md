# WSL2 部署指南

## 一、WSL 简介[​](https://docs.eesast.com/docs/tools/wsl#wsl-%E7%AE%80%E4%BB%8B "Direct link to WSL 简介")

WSL（Windows Subsyetem for Linux，适用于 Linux 的 Windows 子系统），是 Microsoft 公司于 2016 年在 Windows 10 平台发布的一项功能，其使得用户可以在 Windows 操作系统上运行 ELF 格式的 Linux 可执行文件。

WSL 目前已发布两代产品：WSL 1 和 WSL 2。WSL 1 实现了 Linux 兼容层，将 Linux 系统调用转换为 Windows NT 系统调用；而 WSL 2 则利用 Windows 的 Hyper-V 功能，通过虚拟化技术直接运行 Linux 虚拟机，更接近原生 Linux 操作系统体验。

**注意**：WSL 2 并不是 WSL 1 的升级版本，因此安装 WSL 2 不需要先安装 WSL 1

## 二、安装

### 1. 检查 Windows 版本[​](https://docs.eesast.com/docs/tools/wsl#%E7%AC%AC%E4%B8%80%E6%AD%A5%E6%A3%80%E6%9F%A5-windows-%E7%89%88%E6%9C%AC "Direct link to 第一步：检查 Windows 版本")

WSL 2 需要 **Windows 10 1903** （内部版本 18362）或更高版本（x64）。如果版本较低，请更新 Windows 10 系统。

- `开始 -> 设置 -> 系统 -> 关于`

### 2. 检查 BIOS 是否开启了虚拟化[​](https://docs.eesast.com/docs/tools/wsl#%E7%AC%AC%E4%BA%8C%E6%AD%A5%E6%A3%80%E6%9F%A5-bios-%E6%98%AF%E5%90%A6%E5%BC%80%E5%90%AF%E4%BA%86%E8%99%9A%E6%8B%9F%E5%8C%96 "Direct link to 第二步：检查 BIOS 是否开启了虚拟化")

菜单栏邮件打开任务管理器，进入“性能”，查看“CPU”，如果虚拟化显示已启用则说明满足要求，否则需要进入BIOS设置。

### 3. 选择发行版并安装

```bash
# 查看发行版
wsl --list --online
# 选择发行版并安装
wsl --install -d Ubuntu-22.04
# 列出已安装发行版
wsl --list
# 查看 WSL 版本
wsl -l -v
# 切换WSL版本2
wsl --set-default-version 2
```

### 4. 配置代理

参考资料： [配置WSL2使用本机v2ray代理新手保姆教程 - VPS部落](https://ivpsr.com/2484.html)
