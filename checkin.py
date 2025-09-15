
import requests
import re
import os

def check_in():
    """
    自动签到函数
    """
    try:
        # 获取脚本所在的目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        cookie_file_path = os.path.join(script_dir, 'checkin.txt')

        # 从 checkin.txt 读取 cookie
        with open(cookie_file_path, 'r') as f:
            cookie_content = f.readline().strip()

        # 提取 b2_token
        match = re.search(r'b2_token=([^;]+)', cookie_content)
        if not match:
            print("错误：在 checkin.txt 中未找到 b2_token。")
            return

        token = match.group(1)

        # 请求头
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Authorization': f'Bearer {token}',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Cookie': cookie_content,
            'Origin': 'https://luolcy.com',
            'Referer': 'https://luolcy.com/mission/today',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        # 直接执行签到
        print("正在执行签到...")
        checkin_url = "https://luolcy.com/wp-json/b2/v1/userMission"
        response = requests.post(checkin_url, headers=headers)

        # 检查响应
        if response.status_code == 200:
            try:
                response_data = response.json()
                # 成功的响应是一个包含积分信息的字典
                if isinstance(response_data, dict) and 'credit' in response_data:
                    new_credit = response_data['credit']
                    print(f"签到成功！当前积分：{new_credit}")
                # 兼容旧的“已签到”判断
                elif '您今天已经签到过了' in response.text:
                    print("您今天已经签到过了。")
                # 兼容返回纯数字积分的情况
                elif str(response_data).isdigit():
                    print(f"签到完成！当前积分：{response_data}")
                else:
                    print(f"签到失败，响应未知：{response.text}")
            except ValueError:
                # 如果不是JSON，则可能是文本提示
                if '您今天已经签到过了' in response.text:
                    print("您今天已经签到过了。")
                else:
                    print(f"签到失败，无法解析服务器响应：{response.text}")
        else:
            print(f"签到请求失败，状态码：{response.status_code}")
            print(f"响应内容：{response.text}")

    except FileNotFoundError:
        print(f"错误：找不到 checkin.txt 文件。请确保它和脚本在同一个目录下。")
    except Exception as e:
        print(f"发生了一个错误：{e}")

if __name__ == "__main__":
    check_in()
