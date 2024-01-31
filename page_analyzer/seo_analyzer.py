from bs4 import BeautifulSoup
import requests


def get_page_content(url):
    status_code, text = 0, ''
    try:
        response = requests.get(url)
        status_code = response.status_code
        text = response.text
    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.InvalidSchema):
        pass
    finally:
        return status_code, text


def get_seo_info_by_content(text):
    result = {}
    soup = BeautifulSoup(text, "html.parser")
    if soup.h1:
        result['h1'] = soup.h1.string
    if soup.title:
        result['title'] = soup.title.string
    description = soup.find(
        "meta", {"name": "description"})
    if description:
        result['description'] = description.get("content")

    return result


def get_seo_info(url):
    result = {'result': False}
    status_code, text = get_page_content(url)

    result['status_code'] = status_code
    if text:
        result['result'] = True
        seo_info = get_seo_info_by_content(text)
        result.update(seo_info)
    return result
