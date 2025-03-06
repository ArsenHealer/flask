from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Путь к файлу логов
LOG_FILE_PATH = "/shavol/access.log"

@app.route('/')
def get_ip():
    # Получаем IP-адрес из заголовка X-Forwarded-For, если он есть
    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        client_ip = request.remote_addr
    return f"Ваш IP-адрес: {client_ip}"

@app.route('/logs')
def show_logs():
    # Проверяем, существует ли файл логов
    if not os.path.exists(LOG_FILE_PATH):
        return "Логи не найдены", 404

    # Читаем логи из файла
    with open(LOG_FILE_PATH, 'r') as log_file:
        logs = log_file.readlines()

    # Отображаем логи в HTML
    log_html = "<h1>Логи Nginx</h1><ul>"
    for log in logs:
        log_html += f"<li>{log}</li>"
    log_html += "</ul>"

    return render_template_string(log_html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)