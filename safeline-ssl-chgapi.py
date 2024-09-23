import requests
import json
import urllib3
import argparse
import os
import sys

# 禁用 SSL 警告
urllib3.disable_warnings()

# 定义默认值
DEFAULT_BASE_URL = "https://xxx.com:9443"  # 默认 API 基本 URL
DEFAULT_API_TOKEN = "qt8DjIyqxxxxxxxxxxxxxxxxxxxFD2kOzm-"                    # 默认 API Token
DEFAULT_CERT_ID = 1                                     # 默认证书 ID
DEFAULT_CERT_FILE_PATH = "/data/ssl/live/xxxx.com/fullchain.pem"  # 默认证书文件路径
DEFAULT_CERT_KEY_PATH = "/data/ssl/live/xxxx.com/privkey.pem"      # 默认密钥文件路径

class SafeLine:
    def __init__(self, base_url, api_token):
        self.base_url = base_url
        self.api_token = api_token
        self.session = requests.Session()
        self.session.verify = False
        self.headers = {
            "X-SLCE-API-TOKEN": self.api_token
        }

    def list_all_certs(self):
        """获取证书列表"""
        response = self.session.get(f"{self.base_url}/api/open/cert", headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"无法获取证书列表，状态码: {response.status_code}")
        
        data = response.json()
        if 'data' in data and 'nodes' in data['data']:
            return data['data']['nodes']
        else:
            raise Exception("获取证书列表失败！返回的数据格式不正确")

    def update_cert(self, cert_id, crt, key):
        """更新指定ID的证书"""
        payload = {
            "id": cert_id,
            "manual": {
                "crt": crt,
                "key": key
            },
            "type": 2  # 手动管理的证书
        }

        # 证书更新请求
        response = self.session.put(f"{self.base_url}/api/open/cert/{cert_id}", headers=self.headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"证书更新失败，状态码: {response.status_code}")

        data = response.json()
        if data.get('err') is None:
            print(f"证书 ID 为 {cert_id} 的证书已成功更新。")
        else:
            print(f"证书更新失败: {data.get('err')}")
            raise Exception("更新证书失败")


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='Safeline API 操作脚本', formatter_class=argparse.RawTextHelpFormatter)

    # 基本信息
    parser.add_argument('--base-url', default=DEFAULT_BASE_URL, help=f'API 基本 URL (默认: {DEFAULT_BASE_URL})')
    parser.add_argument('--api-token', default=DEFAULT_API_TOKEN, help=f'API Token')
    parser.add_argument('--cert-id', type=int, default=DEFAULT_CERT_ID, help=f'要更新的证书ID (默认: {DEFAULT_CERT_ID})')
    parser.add_argument('--cert-file', default=DEFAULT_CERT_FILE_PATH, help=f'证书文件路径 (默认: {DEFAULT_CERT_FILE_PATH})')
    parser.add_argument('--key-file', default=DEFAULT_CERT_KEY_PATH, help=f'证书密钥文件路径 (默认: {DEFAULT_CERT_KEY_PATH})')

    # 选择操作
    subparsers = parser.add_subparsers(dest='command', help='命令')

    # 查看证书列表命令
    subparsers.add_parser('list-certs', help='查看所有证书')

    # 更新证书命令
    update_parser = subparsers.add_parser('update-cert', help='更新证书')
    update_parser.add_argument('--base-url', default=DEFAULT_BASE_URL, help=f'API 基本 URL (默认: {DEFAULT_BASE_URL})')
    update_parser.add_argument('--api-token', default=DEFAULT_API_TOKEN, help=f'API Token')
    update_parser.add_argument('--cert-id', type=int, default=DEFAULT_CERT_ID, help=f'要更新的证书ID (默认: {DEFAULT_CERT_ID})')
    update_parser.add_argument('--cert-file', default=DEFAULT_CERT_FILE_PATH, help=f'证书文件路径 (默认: {DEFAULT_CERT_FILE_PATH})')
    update_parser.add_argument('--key-file', default=DEFAULT_CERT_KEY_PATH, help=f'证书密钥文件路径 (默认: {DEFAULT_CERT_KEY_PATH})')

    return parser, update_parser


def main():
    # 解析命令行参数
    parser, update_parser = parse_arguments()
    args = parser.parse_args()

    # 如果没有命令，则显示 update-cert 的帮助信息
    if not args.command:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # 实例化 SafeLine 类
    safeline = SafeLine(base_url=args.base_url, api_token=args.api_token)

    if args.command == 'list-certs':
        # 打印当前证书列表
        try:
            certs = safeline.list_all_certs()
            print("证书列表：")
            for cert in certs:
                print(f"证书ID: {cert['id']}, 证书信息: {cert}")
        except Exception as e:
            print(f"获取证书列表时发生错误: {e}")

    elif args.command == 'update-cert':
        # 如果参数使用默认值且默认路径正确，程序可直接执行
        try:
            if not os.path.exists(args.cert_file) or not os.path.exists(args.key_file):
                raise FileNotFoundError("证书文件或密钥文件不存在，请检查路径。")

            # 读取证书文件和密钥
            with open(args.cert_file, 'r') as cert_file:
                cert_str = cert_file.read()
            with open(args.key_file, 'r') as key_file:
                cert_key = key_file.read()

            # 强制更新指定的证书
            safeline.update_cert(cert_id=args.cert_id, crt=cert_str, key=cert_key)

        except Exception as e:
            print(f"更新证书时发生错误: {e}")


if __name__ == '__main__':
    main()
