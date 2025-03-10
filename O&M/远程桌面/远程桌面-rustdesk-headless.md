# ubunut headless 远程桌面快速开始

## 开始

### 安装依赖

- 安装 依赖

```bash
# for Ubuntu
apt install ubuntu-desktop              # 桌面
apt install xserver-xorg-video-dummy    # 虚拟诱骗器
apt install lightdm                        # 非必需
```

- 设置密码

```bash
rustdesk --password <password>
```

- 配置诱骗器

```bash
vim /etc/X11/xorg.conf
```

填入以下内容

```bash
Section "ServerFlags"
  Option "DontVTSwitch" "true"
  Option "AllowMouseOpenFail" "true"
  Option "PciForceNone" "true"
  Option "AutoEnableDevices" "false"
  Option "AutoAddDevices" "false"
EndSection

Section "InputDevice"
  Identifier "dummy_mouse"
  Option "CorePointer" "true"
  Driver "void"
EndSection

Section "InputDevice"
  Identifier "dummy_keyboard"
  Option "CoreKeyboard" "true"
  Driver "void"
EndSection

Section "Device"
  Identifier "dummy_videocard"
  Driver "dummy"
  Option "ConstantDPI" "true"
  #VideoRam 4096000
  VideoRam 256000
  #VideoRam 192000
EndSection

Section "Monitor"
  Identifier "dummy_monitor"
  HorizSync   5.0 - 1000.0
  VertRefresh 5.0 - 200.0
  #To add your own modes here, use a modeline calculator, like:
  #http://xtiming.sourceforge.net/cgi-bin/xtiming.pl
  #or using the "gtf" command line tool (http://gtf.sourceforge.net/)

  #This can be used to get a specific DPI, but only for the default resolution:
  #DisplaySize 508 317
  #NOTE: the highest modes will not work without increasing the VideoRam
  # for the dummy video card.
  Modeline "32768x32768" 15226.50 32768 35800 39488 46208 32768 32771 32781 32953
  Modeline "32768x16384" 7516.25 32768 35544 39192 45616 16384 16387 16397 16478
  Modeline "16384x8192" 2101.93 16384 16416 24400 24432 8192 8390 8403 8602
  Modeline "8192x4096" 424.46 8192 8224 9832 9864 4096 4195 4202 4301
  Modeline "6400x2160" 160.51 6400 6432 7040 7072 2160 2212 2216 2269
  Modeline "5680x1440" 142.66 5680 5712 6248 6280 1440 1474 1478 1513
  Modeline "5496x1200" 199.13 5496 5528 6280 6312 1200 1228 1233 1261
  Modeline "5280x1080" 169.96 5280 5312 5952 5984 1080 1105 1110 1135
  Modeline "5280x1200" 191.40 5280 5312 6032 6064 1200 1228 1233 1261
  Modeline "5120x3200" 199.75 5120 5152 5904 5936 3200 3277 3283 3361
  Modeline "4800x1200" 64.42 4800 4832 5072 5104 1200 1229 1231 1261
  Modeline "4720x3840" 227.86 4720 4752 5616 5648 3840 3933 3940 4033
  Modeline "3840x2880" 133.43 3840 3872 4376 4408 2880 2950 2955 3025
  Modeline "3840x2560" 116.93 3840 3872 4312 4344 2560 2622 2627 2689
  Modeline "3840x2048" 91.45 3840 3872 4216 4248 2048 2097 2101 2151
  Modeline "3840x1200" 108.89 3840 3872 4280 4312 1200 1228 1232 1261
  Modeline "3840x1080" 100.38 3840 3848 4216 4592 1080 1081 1084 1093
  Modeline "3864x1050" 338.00 3864 4112 4520 5176 1050 1053 1063 1089
  Modeline "3600x1200" 106.06 3600 3632 3984 4368 1200 1201 1204 1214
  Modeline "3600x1080" 91.02 3600 3632 3976 4008 1080 1105 1109 1135
  Modeline "3520x1196" 99.53 3520 3552 3928 3960 1196 1224 1228 1256
  Modeline "3360x1050" 293.75 3360 3576 3928 4496 1050 1053 1063 1089
  Modeline "3288x1080" 39.76 3288 3320 3464 3496 1080 1106 1108 1135
  Modeline "3120x1050" 272.75 3120 3320 3648 4176 1050 1053 1063 1089
  Modeline "2728x1680" 148.02 2728 2760 3320 3352 1680 1719 1726 1765
  Modeline "2048x2048" 49.47 2048 2080 2264 2296 2048 2097 2101 2151
  Modeline "2048x1536" 80.06 2048 2104 2312 2576 1536 1537 1540 1554
  Modeline "2048x1152" 197.97 2048 2184 2408 2768 1152 1153 1156 1192
  Modeline "2560x1600" 47.12 2560 2592 2768 2800 1600 1639 1642 1681
  Modeline "2560x1440" 42.12 2560 2592 2752 2784 1440 1475 1478 1513
  Modeline "1920x1440" 69.47 1920 1960 2152 2384 1440 1441 1444 1457
  Modeline "1920x1200" 26.28 1920 1952 2048 2080 1200 1229 1231 1261
  Modeline "1920x1080" 23.53 1920 1952 2040 2072 1080 1106 1108 1135
  Modeline "1680x1050" 20.08 1680 1712 1784 1816 1050 1075 1077 1103
  Modeline "1600x1200" 22.04 1600 1632 1712 1744 1200 1229 1231 1261
  Modeline "1600x900" 33.92 1600 1632 1760 1792 900 921 924 946
  Modeline "1440x900" 30.66 1440 1472 1584 1616 900 921 924 946
  ModeLine "1366x768" 72.00 1366 1414 1446 1494  768 771 777 803
  Modeline "1280x1024" 31.50 1280 1312 1424 1456 1024 1048 1052 1076
  Modeline "1280x800" 24.15 1280 1312 1400 1432 800 819 822 841
  Modeline "1280x768" 23.11 1280 1312 1392 1424 768 786 789 807
  Modeline "1360x768" 24.49 1360 1392 1480 1512 768 786 789 807
  Modeline "1024x768" 18.71 1024 1056 1120 1152 768 786 789 807
  Modeline "768x1024" 19.50 768 800 872 904 1024 1048 1052 1076
EndSection

Section "Screen"
  Identifier "dummy_screen"
  Device "dummy_videocard"
  Monitor "dummy_monitor"
  DefaultDepth 24
  SubSection "Display"
    Viewport 0 0
    Depth 24
    #Modes "32768x32768" "32768x16384" "16384x8192" "8192x4096" "5120x3200" "3840x2880" "3840x2560" "3840x2048" "2048x2048" "2560x1600" "1920x1440" "1920x1200" "1920x1080" "1600x1200" "1680x1050" "1600x900" "1400x1050" "1440x900" "1280x1024" "1366x768" "1280x800" "1024x768" "1024x600" "800x600" "320x200"
    Modes "5120x3200" "3840x2880" "3840x2560" "3840x2048" "2048x2048" "2560x1600" "1920x1440" "1920x1200" "1920x1080" "1600x1200" "1680x1050" "1600x900" "1400x1050" "1440x900" "1280x1024" "1366x768" "1280x800" "1024x768" "1024x600" "800x600" "320x200"
    #Virtual 32000 32000
    #Virtual 16384 8192
    #Virtual 8192 4096
    #Virtual 5120 3200
    Virtual 1024 768
  EndSubSection
EndSection

Section "ServerLayout"
  Identifier   "dummy_layout"
  Screen       "dummy_screen"
  InputDevice  "dummy_mouse"
  InputDevice  "dummy_keyboard"
EndSection
```

- 确认显示器存在

```bash
export DISPLAY=:0

xrandr -q
```

- 调整分辨率

```bash
export DISPLAY=:0

xrandr --output DUMMY0 --mode 1024x768
```

### 配置 rustdesk

- 启动 headless

```bash
sudo rustdesk --option allow-linux-headless Y
# 获取连线
sudo rustdesk --get-id
# 设置密码
sudo rustdesk --password "密碼"
```

## 参考资料

- 配置虚拟显示器

[用RustDesk連線到headless的樹莓派Linux伺服器 &#183; Ivon的部落格](https://ivonblog.com/posts/rustdesk-connect-to-linux-headless-server/)
