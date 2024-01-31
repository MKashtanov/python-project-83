from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from page_analyzer.repository import UrlsRepository
from page_analyzer.validator import validate, normalize_url, crop_str
from page_analyzer.seo_analyzer import get_seo_info
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
    return render_template(
        'index.html',
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
    url_item, result_add = repo.add_url(normalized_url)
    if result_add:
        flash('Страница успешно добавлена', 'success')
    else:
        flash('Страница уже существует', 'info')
    url_id = url_item.id
    return redirect(url_for('get_url_view', id=url_id))


@app.route('/urls')
def get_urls():
    return render_template(
        'urls.html',
        url_items=repo.get_all_url(),
    )


@app.route('/urls/<int:id>')
def get_url_view(id):
    url_item = repo.find_url_by_id(id)
    checks = repo.find_checks_by_url_id(id)
    if url_item:
        return render_template(
            'url.html',
            url_item=url_item,
            checks=checks,
        )
    return render_template('404.html'), 404


@app.post('/urls/<int:id>/checks')
def do_url_check(id):
    url_item = repo.find_url_by_id(id)
    if not url_item:
        return render_template('404.html'), 404

    result = False
    url = url_item.name
    result_check = get_seo_info(url)
    if result_check['status_code'] == 200:
        result_check['h1'] = crop_str(result_check.get('h1', ''), 255)
        result_check['title'] = crop_str(result_check.get('title', ''), 255)
        result_check['description'] = crop_str(result_check.get('description', ''), 255)
        result = repo.add_check(url, result_check)
    if result:
        flash('Страница успешно проверена', 'success')
    else:
        flash('Произошла ошибка при проверке', 'danger')
    return redirect(url_for('get_url_view', id=id))
