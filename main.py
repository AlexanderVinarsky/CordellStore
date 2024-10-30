import requests

cookies = {
    '_ga': 'GA1.1.860917445.1730309330',
    '_ym_uid': '1730309331268901850',
    '_ym_d': '1730309331',
    '_ym_isad': '1',
    '_ym_visorc': 'b',
    'nmg_udi': '4545CF1C-9D97-E5ED-C6C2-CE1D3DBA0DB2',
    'x_device_id': '4545CF1C-9D97-E5ED-C6C2-CE1D3DBA0DB2',
    'shopCode': '992301',
    'x_shop_type': 'ME',
    'PHPSESSID': 'isk7mh3ikbsscvta83ecgev03k',
    '_ga_L0N0B74HJP': 'GS1.1.1730309329.1.1.1730309691.60.0.0',
    'nmg_sp': 'Y',
}

headers = {
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://magnit.ru',
    'Referer': 'https://magnit.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'accept': 'application/json',
    'content-type': 'application/json',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'x-app-version': '7.0.0',
    'x-client-name': 'magnit',
    'x-device-id': '4545CF1C-9D97-E5ED-C6C2-CE1D3DBA0DB2',
    'x-device-platform': 'Web',
    'x-device-tag': 'disabled',
    'x-new-magnit': 'true',
    'x-platform-version': 'Windows Chrome 132',
}

json_data = {
    'aggs': False,
    'geoBoundingBox': {
        'leftTopLatitude': 45.09625768514569,
        'leftTopLongitude': 38.93551992034913,
        'rightBottomLatitude': 45.03792733446187,
        'rightBottomLongitude': 39.01148007965087,
    },
    'limit': 5000,
    'storeTypes': [
        1,
        2,
        6,
        5,
    ],
}

response = requests.post('https://magnit.ru/webgate/v1/store-search/geo', cookies=cookies, headers=headers, json=json_data)
print(response.text)