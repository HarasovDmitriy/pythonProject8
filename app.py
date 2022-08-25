from flask import Flask, request, render_template, send_from_directory
from functions import load_all_post, search_post
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.ERROR)

POST_PATH = "posts.json"
posts = load_all_post(POST_PATH)
UPLOAD_FOLDER = "../uploads/images/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)


@app.route("/", methods=['GET', "POST"])
def page_index():
    return render_template("index.html")


@app.route("/post_list")
def page_tag():
    s = request.args['s']
    items = search_post(s, posts)
    logging.info("Выполнен поиск")
    return render_template("post_list.html", s=s, search_posts=items)


@app.route("/post_form", methods=["GET", "POST"])
def page_post_form():
    return render_template("post_form.html")


@app.route("/post_uploaded", methods=["POST"])
def page_post_upload():
    """ Эта вьюшка обрабатывает форму"""
    if request.files.get("pic") and request.form["content"]:
        picture = request.files.get("pic")
        content = request.form["content"]
        filename = picture.filename
        extension = filename.split(".")[-1]
        if extension in ALLOWED_EXTENSIONS:
            picture.save(f"./uploads/images/{filename}")
            path = Path('posts.json')
            data = json.loads(path.read_text(encoding='utf-8'))
            data.append({'pic': f'{UPLOAD_FOLDER}{filename}', 'content': content})
            path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8', )
            return render_template("post_uploaded.html", pic=f"./uploads/images/{filename}", content=content)
        logging.info("загруженный файл- не картинка")
        return f"Тип файлов {extension} не поддерживается"
    logging.error("ошибка при загрузке файла")
    return f"Вы забыли загрузить картинку или текст"


@app.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("uploads", path)


app.run()

