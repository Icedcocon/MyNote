# Wake-on-LAN-wol快速开始

## 一、环境配置

### 1. 服务机配置

- 查看 `Wake-on` 选项： 如果为 d 则为关闭； 如果为 g 则为开启

```bash
root@beijing-ubuntu:~# ethtool enp41s0
Settings for enp41s0:
        Supported ports: [ TP    MII ]
        Supported link modes:   10baseT/Half 10baseT/Full
                                100baseT/Half 100baseT/Full
                                1000baseT/Full
        Supported pause frame use: Symmetric Receive-only
        Supports auto-negotiation: Yes
        Supported FEC modes: Not reported
        Advertised link modes:  10baseT/Half 10baseT/Full
                                100baseT/Half 100baseT/Full
                                1000baseT/Full
        Advertised pause frame use: Symmetric Receive-only
        Advertised auto-negotiation: Yes
        Advertised FEC modes: Not reported
        Link partner advertised link modes:  10baseT/Half 10baseT/Full
                                             100baseT/Half 100baseT/Full
                                             1000baseT/Half 1000baseT/Full
        Link partner advertised pause frame use: No
        Link partner advertised auto-negotiation: Yes
        Link partner advertised FEC modes: Not reported
        Speed: 1000Mb/s
        Duplex: Full
        Auto-negotiation: on
        master-slave cfg: preferred slave
        master-slave status: slave
        Port: Twisted Pair
        PHYAD: 0
        Transceiver: external
        MDI-X: Unknown
        Supports Wake-on: pumbg
        Wake-on: g
        Link detected: yes
```

- 开启 wol

```bash
ethtool -s enp41s0 wol g
```

- 持久化 `/etc/systemd/system/wol.service`

```systemd
[Unit]
Description=Enable Wake-on-LAN for enp41s0
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/sbin/ethtool -s enp41s0 wol g

[Install]
WantedBy=multi-user.target
```

### 2. 客户机配置

```bash
apt install  etherwake
etherwake -i br0 $MAC_ADDRESS
```

## 参考资料
