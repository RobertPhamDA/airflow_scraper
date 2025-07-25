import pandas as pd
import requests
import time
import random
from sqlalchemy import create_engine
import os


def extract_products_id_tiki():
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://tiki.vn/?src=header_tiki',
    'x-guest-token': '8jWSuIDBb2NGVzr6hsUZXpkP1FRin7lY',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
    }

    params = {
        'limit': '48',
        'include': 'sale-attrs,badges,product_links,brand,category,stock_item,advertisement',
        'aggregations': '1',
        'trackity_id': '70e316b0-96f2-dbe1-a2ed-43ff60419991',
        'category': '1883',
        'page': '1',
        'src': 'c1883',
        'urlKey':  'nha-cua-doi-song',
    }

    product_id = []
    for i in range(1, 11):
        params['page'] = i
        response = requests.get('https://tiki.vn/api/v2/products', headers=headers, params=params)#, cookies=cookies)
        if response.status_code == 200:
            print('request success!!!')
            for record in response.json().get('data'):
                product_id.append({'id': record.get('id')})
        time.sleep(random.randrange(3, 10))

    df = pd.DataFrame(product_id)
    df['insertedDate'] = pd.to_datetime('today').strftime('%Y-%m-%d %H:%M:%S')
    df = df.drop_duplicates(subset=['id'])
    return df

def load_to_postgres_tiki_product_id(df: pd.DataFrame):
    db_user = os.getenv("POSTGRES_USER", "airflow")
    db_pass = os.getenv("POSTGRES_PASSWORD", "airflow")
    db_host = os.getenv("POSTGRES_HOST", "postgres")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB", "airflow")

    engine = create_engine(f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")
    df.to_sql("tiki_product_id", engine, if_exists="replace", index=False)
