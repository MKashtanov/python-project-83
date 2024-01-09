from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    # Получить доступ к содержимому запроса можно через специальный объект request
    if request.method == 'POST':
        return 'Hello, POST!'
    return 'Hello, GET!'
