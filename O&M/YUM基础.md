# yum 安裝指定版本套件

### yum安装步骤

- 确认可用版本： `yum list redis --showduplicates`

- 版本信息拆解：`{package name}.{arch} {version}-{release} {repo name}`

- 确认详细信息： `yum info {package name}-{version}-{release}.{arch}`
  
  简易语法确认： `yum info {package name}-{version}`

- 实际安装软件： `yum install -y {package name}-{version}-{release}.{arch}`
  
  简易语法安装： `yum install -y {package name}-{version}`
