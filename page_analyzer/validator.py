from urllib.parse import urlparse, urlunparse
import validators


def validate(url):
    error = ''
    if not validators.url(url):
        error = 'URL не правильный'
        return error
    if len(url) > 255:
        error = 'URL слишком длинный'
    return error


def normalize_url(url):
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    netloc = parsed_url.netloc
    result_url = urlunparse([scheme, netloc, '', '', '', ''])
    return result_url


def crop_str(str_, len_):
    if isinstance(str_, str):
        return str_ if len(str_) <= len_ else f"{str_[:len_ - 3]}..."
    return str_
