# safeline-ssl-chgapi
通过safeline的openapi来更新证书信息，并结合自己基于Let's Encrypt自动获取、续订ssl通配符域名证书的脚本，达到在不对长亭WAF配置做过多改动的情况下，定期自动轮换证书时间，实现一套可用于简单生产级别的WAF系统。

# 如果使用
### 下载safeline-ssl-chgapi.py
### chmod 755 safeline-ssl-chgapi.py
```
# 使用帮助
/ # python3 safeline-ssl-chgapi.py
usage: safeline-ssl-chgapi.py [-h] [--base-url BASE_URL] [--api-token API_TOKEN] [--cert-id CERT_ID] [--cert-file CERT_FILE] [--key-file KEY_FILE] {list-certs,update-cert} ...

Safeline API 操作脚本

positional arguments:
  {list-certs,update-cert}
                        命令
    list-certs          查看所有证书
    update-cert         更新证书

optional arguments:
  -h, --help            show this help message and exit
  --base-url BASE_URL   API 基本 URL (默认: https://xxx.com:9443)
  --api-token API_TOKEN
                        API Token
  --cert-id CERT_ID     要更新的证书ID (默认: 1)
  --cert-file CERT_FILE
                        证书文件路径 (默认: /data/ssl/live/xxx.com/fullchain.pem)
  --key-file KEY_FILE   证书密钥文件路径 (默认: /data/ssl/live/xxx.com/privkey.pem)

#获取所有证书信息
/ # python3 safeline-ssl-chgapi.py list-certs
证书列表：
证书ID: 2, 证书信息: {'id': 2, 'domains': ['*.xxx.com', 'xxx.com'], 'issuer': 'R11', 'self_signature': False, 'trusted': False, 'revoked': False, 'expired': False, 'type': 2, 'acme_message': '', 'valid_before': '2024-12-11T00:11:14+08:00', 'related_sites': ['雷池控制台', 'xxx.com', 'hubproxy.xxx.com']}
证书ID: 1, 证书信息: {'id': 1, 'domains': ['*.yyy.com', 'yyy.com'], 'issuer': 'R10', 'self_signature': False, 'trusted': False, 'revoked': False, 'expired': False, 'type': 2, 'acme_message': '', 'valid_before': '2024-12-04T23:07:20+08:00', 'related_sites': ['blog.yyy.com', 'yyy.com']}

#更新证书信息
/ # python3 safeline-ssl-chgapi.py update-cert --base-url https://xxx.com:9443 --api-token qt8DjIyqxxxxxxxxxxxxxxxxxxxFD2kOzm- --cert-id 2 --cert-file /data/ssl/live/smszhd.com/fullchain.pem --key-file /data/ssl/live/smszhd.com/privkey.pem
证书 ID 为 2 的证书已成功更新。
```
