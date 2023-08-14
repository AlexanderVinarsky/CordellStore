import requests

cookies = {
    'PHPSESSID': 'pag7glnm88dcsii966i03tjjga',
    'x_device_id': 'zz7uenrw3f',
    'BX_USER_ID': '62b404e0d4b3d95c09c55960e89eb188',
    'tmr_lvid': '5bfee37c49b6660335d07733d490673b',
    'tmr_lvidTS': '1692026339540',
    '_ym_uid': '1692026340945011940',
    '_ym_d': '1692026340',
    '_ga': 'GA1.2.844146411.1692026340',
    '_gid': 'GA1.2.1786822321.1692026340',
    '_gat_UA-61230203-9': '1',
    '_gat_UA-61230203-3': '1',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
    '_clck': '1b5qfdc|2|fe5|0|1321',
    'mg_foradult': 'true',
    'tmr_detect': '1%7C1692026347817',
    '_ga_764JLDFS07': 'GS1.2.1692026340.1.1.1692026347.53.0.0',
    '_ga_L0N0B74HJP': 'GS1.2.1692026340.1.1.1692026348.52.0.0',
    '_clsk': '1l4fc4e|1692026348677|3|1|y.clarity.ms/collect',
    'mg_geo_id': '1761',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'PHPSESSID=pag7glnm88dcsii966i03tjjga; x_device_id=zz7uenrw3f; BX_USER_ID=62b404e0d4b3d95c09c55960e89eb188; tmr_lvid=5bfee37c49b6660335d07733d490673b; tmr_lvidTS=1692026339540; _ym_uid=1692026340945011940; _ym_d=1692026340; _ga=GA1.2.844146411.1692026340; _gid=GA1.2.1786822321.1692026340; _gat_UA-61230203-9=1; _gat_UA-61230203-3=1; _ym_isad=1; _ym_visorc=w; _clck=1b5qfdc|2|fe5|0|1321; mg_foradult=true; tmr_detect=1%7C1692026347817; _ga_764JLDFS07=GS1.2.1692026340.1.1.1692026347.53.0.0; _ga_L0N0B74HJP=GS1.2.1692026340.1.1.1692026348.52.0.0; _clsk=1l4fc4e|1692026348677|3|1|y.clarity.ms/collect; mg_geo_id=1761',
    'Referer': 'https://magnit.ru/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'utm_source': 'magnit.ru',
    'utm_campaign': 'catalog',
    'utm_medium': 'allgoods',
}

response = requests.get('https://magnit.ru/catalog/', params=params, cookies=cookies, headers=headers)

print(response.text)