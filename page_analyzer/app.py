from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from . repository import UrlsRepository
from . validator import validate, normalize_url
from . checker import check_url
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

repo = UrlsRepository(DATABASE_URL)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def index():
    url = {}
    return render_template(
        'index.html',
        url=url,
    )


@app.post('/urls')
def add_url():
    data = request.form.to_dict()
    url = data.get('url')
    error = validate(url)
    if error:
        flash('Некорректный URL', 'danger')
        return render_template(
            'index.html',
            url=url,
        ), 422
    normalized_url = normalize_url(url)
    url_item = repo.find_one_url(name=normalized_url)
    if not url_item:
        url_item = repo.add_url(normalized_url)
        flash('Страница успешно добавлена', 'success')
    else:
        flash('Страница уже существует', 'info')
    url_id = url_item.id
    return redirect(url_for('url_view', id=url_id))


@app.route('/urls')
def urls():
    return render_template(
        'urls.html',
        url_items=repo.get_all_url(),
    )


@app.route('/urls/<int:id>')
def url_view(id):
    url_item = repo.find_one_url(id=id)
    checks = repo.find_checks(id=id)
    if url_item:
        return render_template(
            'url.html',
            url_item=url_item,
            checks=checks,
        )
    return render_template(
           'not_found.html',
    ), 404


@app.post('/urls/<int:id>/checks')
def url_check(id):
    result = False
    url_item = repo.find_one_url(id=id)
    if url_item:
        url = url_item.name
        result_check = check_url(url)
        print('url =', url, 'r_ch =', result_check)
        if result_check['result']:
            result = repo.add_check(url, result_check)
    if result:
        flash('Страница успешно проверена', 'success')
    else:
        flash('Произошла ошибка при проверке', 'danger')
    return redirect(url_for('url_view', id=id))
