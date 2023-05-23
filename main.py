import datetime
import io
import json
import os

import requests

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def get_data(num: int, code: str, qType: str):
    url = "https://reportapi.eastmoney.com/report/list"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    params = {
        'cb': 'datatable7539582',
        'industryCode': '*',
        'pageSize': "100",  # 每页显示的数量
        'industry': '*',
        'rating': '*',
        'ratingChange': '*',
        'beginTime': '2021-07-01',
        'endTime': datetime.datetime.now().strftime("%Y-%m-%d"),
        'pageNo': '1',  # 当前页码
        'qType': '1',
        'orgCode': '*',
        'code': '*',
        'rcode': '*',
        'p': '2',
        'pageNum': '2',
        'pageNumber': '2',
        '_': '1684802657014',
    }
    if qType == "stock" or qType == "0":
        params['qType'] = 0
    elif qType == "industry" or qType == "1":
        params['qType'] = 1

    if code != "":
        params['code'] = code
        params['qType'] = '0'

    if num <= 100:
        params['pageSize'] = str(num)
        response = requests.request("GET", url, headers=headers, params=params)
        response_text = response.text[len(params['cb']) + 1:-1]
        response_json = json.loads(response_text)
        return response_json['data'][:num]
    else:
        i = 1
        __data = []
        nums = num
        while True:
            params['pageNo'] = str(i)
            response = requests.request("GET", url, headers=headers, params=params)
            response_text = response.text[len(params['cb']) + 1:-1]
            response_json = json.loads(response_text)
            __data += response_json['data']
            if len(response_json['data']) < 100 or num <= 100:
                break
            i += 1
            num -= 100
        return __data[:nums]


def download_pdf(save_path, pdf_name, pdf_url):
    send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8"}
    __response = requests.get(pdf_url, headers=send_headers)
    bytes_io = io.BytesIO(__response.content)
    with open(os.path.join(save_path, pdf_name + ".pdf"), mode='wb') as f:
        f.write(bytes_io.getvalue())
        print(f'{pdf_name} is downloaded')


if __name__ == '__main__':
    data = get_data(10, "600111", "1")
    # 对数组进行遍历
    print("--------------------------------------------------")
    for item in data:
        print(item['title'])
        print(item['infoCode'])
        print(item['stockName'])
        print(item['industryName'])
        print(item['orgSName'])
        print(item['orgCode'])
        print(item['publishDate'])
        print("--------------------------------------------------")
        download_pdf(
            save_path=f'{THIS_DIR}/tmp/',
            pdf_name=item['title'].replace('/', '／').replace('\\', '＼'),
            pdf_url="https://pdf.dfcfw.com/pdf/H3_" + item['infoCode'] + "_1.pdf"
        )
