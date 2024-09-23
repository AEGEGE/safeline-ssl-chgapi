# safeline-ssl-chgapi
Update certificate information through safeline's openapi, and combine it with your own script based on Let's Encrypt to automatically obtain and renew ssl wildcard domain name certificates, so as to automatically rotate the certificate time regularly without making too many changes to Changting WAF configuration, so as to achieve a WAF system that can be used for simple production level.

# How to use
Download safeline-ssl-chgapi.py
chmod 755 safeline-ssl-chgapi.py
```
# Using Help
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

#Get all certificate information
/ # python3 safeline-ssl-chgapi.py list-certs
证书列表：
证书ID: 2, 证书信息: {'id': 2, 'domains': ['*.xxx.com', 'xxx.com'], 'issuer': 'R11', 'self_signature': False, 'trusted': False, 'revoked': False, 'expired': False, 'type': 2, 'acme_message': '', 'valid_before': '2024-12-11T00:11:14+08:00', 'related_sites': ['雷池控制台', 'xxx.com', 'hubproxy.xxx.com']}
证书ID: 1, 证书信息: {'id': 1, 'domains': ['*.yyy.com', 'yyy.com'], 'issuer': 'R10', 'self_signature': False, 'trusted': False, 'revoked': False, 'expired': False, 'type': 2, 'acme_message': '', 'valid_before': '2024-12-04T23:07:20+08:00', 'related_sites': ['blog.yyy.com', 'yyy.com']}

#Renewing Certificates
/ # python3 safeline-ssl-chgapi.py update-cert --base-url https://xxx.com:9443 --api-token qt8DjIyqxxxxxxxxxxxxxxxxxxxFD2kOzm- --cert-id 2 --cert-file /data/ssl/live/smszhd.com/fullchain.pem --key-file /data/ssl/live/smszhd.com/privkey.pem
证书 ID 为 2 的证书已成功更新。
```
