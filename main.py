import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse


def shorten_link(url, headers):
  payload = {
    'long_url': url
  }
  url_for_short = 'https://api-ssl.bitly.com/v4/shorten'
  response = requests.post(url_for_short, headers=headers, json=payload)
  response.raise_for_status()

  bitlink = response.json()['id']
  return bitlink


def count_clicks(url, headers):
  parsed_url = urlparse(url)
  bitlink = '{}{}'.format(parsed_url.netloc, parsed_url.path)
  url_for_count = 'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'.format(bitlink=bitlink)
  response = requests.get(url_for_count, headers=headers)
  response.raise_for_status()

  clicks_count = response.json()['total_clicks']
  return clicks_count


if __name__ == '__main__':
  load_dotenv()

  help = '''Cократить ссылку: main.py [ваша ссылка с http:// или https://]
  Узнать количество переходов по битлитнку: main.py [битлинк]'''

  parser = argparse.ArgumentParser()
  parser.add_argument("url", help=help)
  args = parser.parse_args()

  token = os.getenv('BITLY_TOKEN')
  url = args.url
  headers = { 
    'Authorization': 'Bearer {}'.format(token) 
  }

  try:
    try:
      print('Количество кликов:', count_clicks(url, headers))
    except requests.exceptions.HTTPError:
      print('Битлинк', shorten_link(url, headers))
  except requests.exceptions.HTTPError: 
    print('Ошибка')
