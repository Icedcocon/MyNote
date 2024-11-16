# rsync同步服务快速开始

## 一、 脚本配置

### 1. 开始

- 编辑文件 `/etc/systemd/system/disk-sync.service`

> 注意： 请修改 ExecStart 路径及User为实际用户名。

```bash
[Unit]
Description=Disk Synchronization Service
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/sync_disks.sh
User=family
StandardOutput=append:/var/log/disk_sync.log
StandardError=append:/var/log/disk_sync.log

[Install]
WantedBy=multi-user.target
```

- 编辑文件 `/etc/systemd/system/disk-sync.timer`

> 注意请修改 OnCalendar 按需。如
> 
> - OnCalendar=*-*-* 02:00:00 （每天凌晨2点）
> 
> - OnCalendar=Sun *-*-* 02:00:00 （每周日凌晨2点）

```bash
[Unit]
Description=Timer for Disk Synchronization Service

[Timer]
# 每6小时运行一次
OnCalendar=*-*-* 00/6:00:00
# 系统启动后延迟15分钟运行一次
OnBootSec=15min
# 如果错过了预定时间（比如系统关机），系统启动后立即运行
Persistent=true

[Install]
WantedBy=timers.target
```

- 配置脚本 `/usr/local/bin/sync_disks.sh`

```bash
#!/bin/bash

rsync -avz --delete /mnt/DATA-LEFT/Photos/ /mnt/DATA-RIGHT/Backup/
```

- 设置权限

```bash
# 设置脚本执行权限
chmod +x /path/to/sync_disks.sh

# 设置服务文件权限
chmod 644 /etc/systemd/system/disk-sync.service
chmod 644 /etc/systemd/system/disk-sync.timer
```

- 启动服务

```bash
systemctl daemon-reload
systemctl enable disk-sync.timer
systemctl start disk-sync.timer
```

- 其他指令

```bash
# 立即运行同步服务（不等待定时器）
sudo systemctl start disk-sync.service

# 查看服务日志
sudo journalctl -u disk-sync.service

# 查看定时器日志
sudo journalctl -u disk-sync.timer
```
