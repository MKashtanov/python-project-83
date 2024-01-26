from bs4 import BeautifulSoup
import requests


def get_seo_info(url):
    result = {'result': False}
    status_code, text = '', ''
    try:
        response = requests.get(url)
        status_code = response.status_code
        text = response.text
    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.InvalidSchema):
        pass

    if status_code == 200:
        soup = BeautifulSoup(text, "html.parser")
        h1 = soup.h1.string if soup.h1 else None
        title = soup.title.string if soup.title else None
        description = soup.find(
            "meta", {"name": "description"}).get("content")

        result = {
            'result': True,
            'status_code': status_code,
            'h1': h1,
            'title': title,
            'description': description,
        }
    return result
