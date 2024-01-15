from bs4 import BeautifulSoup
import requests


def check_url(url):
    result = {'result': False}
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.string
            description = soup.find(
                "meta", {"name": "description"}).get("content")
            h1 = ""

            result.update({'result': True,
                           'status_code': response.status_code,
                           'h1': h1,
                           'title': title,
                           'description': description,
                           })
    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.InvalidSchema):
        print('Request error', url)

    return result
