import pandas as pd
import requests
from sqlalchemy import create_engine
import os
import time
import random
from sqlalchemy.dialects.postgresql import insert  # import riêng cho PostgreSQL
from sqlalchemy import Table, MetaData


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
    for i in range(1, 21):
        params['page'] = i
        response = requests.get('https://tiki.vn/api/v2/products', headers=headers, params=params)#, cookies=cookies)
        if response.status_code == 200:
            print('request success!!!')
            for record in response.json().get('data'):
                product_id.append({'id': record.get('id')})
        time.sleep(random.randrange(3, 10))

    df = pd.DataFrame(product_id)
    df_product_id = df.drop_duplicates(subset=['id'])
    return df_product_id


def scraper_tiki_product_detail():
    cookies = {
        'TIKI_GUEST_TOKEN': '8jWSuIDBb2NGVzr6hsUZXpkP1FRin7lY',
        'TOKENS': '{%22access_token%22:%228jWSuIDBb2NGVzr6hsUZXpkP1FRin7lY%22%2C%22expires_in%22:157680000%2C%22expires_at%22:1763654224277%2C%22guest_token%22:%228jWSuIDBb2NGVzr6hsUZXpkP1FRin7lY%22}',
        'amp_99d374': 'eSc-_0HT1um7cb57E7dwA0...1enloc6a2.1enlohtdv.3.2.5',
        'amp_99d374_tiki.vn': 'eSc-_0HT1um7cb57E7dwA0...1enloc6a2.1enlocds8.0.1.1',
        '_gcl_au': '1.1.559117409.1605974236',
        '_ants_utm_v2': '',
        '_pk_id.638735871.2fc5': 'b92ae025fbbdb31f.1605974236.1.1605974420.1605974236.',
        '_pk_ses.638735871.2fc5': '*',
        '_trackity': '70e316b0-96f2-dbe1-a2ed-43ff60419991',
        '_ga_NKX31X43RV': 'GS1.1.1605974235.1.1.1605974434.0',
        '_ga': 'GA1.1.657946765.1605974236',
        'ai_client_id': '11935756853.1605974227',
        'an_session': 'zizkzrzjzlzizqzlzqzjzdzizizqzgzmzkzmzlzrzmzgzdzizlzjzmzqzkznzhzhzkzdzhzdzizlzjzmzqzkznzhzhzkzdzizlzjzmzqzkznzhzhzkzdzjzdzhzqzdzizd2f27zdzjzdzlzmzmznzq',
        'au_aid': '11935756853',
        'dgs': '1605974411%3A3%3A0',
        'au_gt': '1605974227146',
        '_ants_services': '%5B%22cuid%22%5D',
        '__admUTMtime': '1605974236',
        '__iid': '749',
        '__su': '0',
        '_bs': 'bb9a32f6-ab13-ce80-92d6-57fd3fd6e4c8',
        '_gid': 'GA1.2.867846791.1605974237',
        '_fbp': 'fb.1.1605974237134.1297408816',
        '_hjid': 'f152cf33-7323-4410-b9ae-79f6622ebc48',
        '_hjFirstSeen': '1',
        '_hjIncludedInPageviewSample': '1',
        '_hjAbsoluteSessionInProgress': '0',
        '_hjIncludedInSessionSample': '1',
        'tiki_client_id': '657946765.1605974236',
        '__gads': 'ID=ae56424189ecccbe-227eb8e1d6c400a8:T=1605974229:RT=1605974229:S=ALNI_MZFWYf2BAjzCSiRNLC3bKI-W_7YHA',
        'proxy_s_sv': '1605976041662',
        'TKSESSID': '8bcd49b02e1e16aa1cdb795c54d7b460',
        'TIKI_RECOMMENDATION': '21dd50e7f7c194df673ea3b717459249',
        '_gat': '1',
        'cto_bundle': 'i6f48l9NVXNkQmJ6aEVLcXNqbHdjcVZoQ0k2clladUF2N2xjZzJ1cjR6WG43UTVaRmglMkZXWUdtRnJTNHZRbmQ4SDAlMkZwRFhqQnppRHFxJTJCSEozZXBqRFM4ZHVxUjQ2TmklMkJIcnhJd3luZXpJSnBpcE1nJTNE',
        'TIKI_RECENTLYVIEWED': '58259141',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://tiki.vn/dien-thoai-samsung-galaxy-m31-128gb-6gb-hang-chinh-hang-p58259141.html?src=category-page-1789&2hi=0',
        'x-guest-token': '8jWSuIDBb2NGVzr6hsUZXpkP1FRin7lY',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    params = (
        ('platform', 'web'),
        ('spid', 187266106)
        #('include', 'tag,images,gallery,promotions,badges,stock_item,variants,product_links,discount_tag,ranks,breadcrumbs,top_features,cta_desktop'),
    )

    def parser_product(json):
        d = dict()
        d['id'] = json.get('id')
        d['sku'] = json.get('sku')
        d['short_description'] = json.get('short_description')
        d['price'] = json.get('price')
        d['list_price'] = json.get('list_price')
        d['price_usd'] = json.get('original_price')
        d['discount'] = json.get('discount')
        d['discount_rate'] = json.get('discount_rate')
        d['review_count'] = json.get('review_count')
        d['order_count'] = json.get('order_count')
        d['inventory_status'] = json.get('inventory_status')
        d['is_visible'] = json.get('is_visible')
        d['stock_item_qty'] = json.get('stock_item').get('qty') if json.get('stock_item') else None
        d['stock_item_max_sale_qty'] = json.get('stock_item').get('max_sale_qty') if json.get('stock_item') else None
        d['product_name'] = json.get('name')
        d['brand_id'] = json.get('brand').get('id') if json.get('brand') else None
        d['brand_name'] = json.get('brand').get('name') if json.get('brand') else None
        return d


    df_id = extract_products_id_tiki()
    p_ids = df_id.id.to_list()
    print(p_ids)
    result = []
    for pid in p_ids:
        response = requests.get('https://tiki.vn/api/v2/products/{}'.format(pid), headers=headers, params=params, cookies=cookies)
        if response.status_code == 200:
            print('Crawl data {} success !!!'.format(pid))
            result.append(parser_product(response.json()))
        # time.sleep(random.randrange(3, 5))
    df_product = pd.DataFrame(result)
    df_product['insertedDate'] = pd.to_datetime('today').strftime('%Y-%m-%d %H:%M:%S')
    df_product = df_product.drop_duplicates(subset=['id'])
    return df_product


def load_to_postgres_tiki_product_detail(df_product: pd.DataFrame):
    db_user = os.getenv("POSTGRES_USER", "airflow")
    db_pass = os.getenv("POSTGRES_PASSWORD", "airflow")
    db_host = os.getenv("POSTGRES_HOST", "postgres")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB", "airflow")

    engine = create_engine(f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")

    metadata = MetaData(bind=engine)
    table = Table('tiki_product_detail', metadata, autoload_with=engine)

    with engine.begin() as conn:
        for row in df_product.to_dict(orient='records'):
            stmt = insert(table).values(**row)
            update_dict = {col.name: stmt.excluded[col.name] for col in table.columns if col.name != 'id'}
            stmt = stmt.on_conflict_do_update(index_elements=['id'], set_=update_dict)
            conn.execute(stmt)