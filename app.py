from flask import Flask, request, render_template, send_from_directory
from functions import load_all_post, search_post
import json
from pathlib import Path

POST_PATH = "posts.json"
posts = load_all_post(POST_PATH)
UPLOAD_FOLDER = "uploads/images"

app = Flask(__name__)


@app.route("/", methods=['GET', "POST"])
def page_index():
    return render_template("index.html")


@app.route("/post_list")
def page_tag():
    s = request.args['s']
    items = search_post(s, posts)
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
        picture.save(f"./uploads/images/{filename}")
        path = Path('posts.json')
        data = json.loads(path.read_text(encoding='utf-8'))
        data.append({'pic': f"../uploads/images/{filename}", 'content': content})
        path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8', )
        return render_template("post_uploaded.html")
    return f"Вы забыли загрузить картинку или текст"





@app.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("uploads", path)


app.run()

