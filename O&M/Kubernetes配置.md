# Kubernetes配置

### Kubernetes配置文件位置及内容

### 访问Kubernetes API

```bash
# 获取证书
clientcert=$(grep client-cert ~/.kube/config |cut -d" " -f 6)
# 获取秘钥
clientkey=$(grep client-key-data ~/.kube/config |cut -d" " -f 6)
# 获取授权
certauth=$(grep certificate-auth ~/.kube/config |cut -d" " -f 6)
# 加密
echo $clientcert | base64 -d > ./client.pem
echo $clientkey | base64 -d > ./client-key.pem
echo $certauth | base64 -d > ./ca.pem
# 查询服务器IP和port
hostPath=$(echo $(kubectl config view |grep server) | cut -d " " -f2)
# 访问API
curl --cert ./client.pem --key ./client-key.pem --cacert ./ca.pem \
${hostPath}/api/v1/pods
```
