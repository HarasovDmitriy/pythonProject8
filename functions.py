import json

from flask import Flask, request, render_template, send_from_directory
from pathlib import Path
from Class import User
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = "../uploads/images/"

def load_all_post(path: str) -> list[User]:
    '''возвращает все посты'''
    arr = []
    data = None

    with open(path, "r", encoding='UTF-8') as f:
        data = json.load(f)

    for item in data:
        pic = item['pic']
        content = item['content']
        arr.append(User(pic, content))

    return arr

def upload_post_user(picture, content):
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
            return render_template("post_uploaded.html")
        return f"Тип файлов {extension} не поддерживается"




def search_post(s: str, arr: list[User]) -> list[User]:
    '''Возвращает пост по поиску
    '''
    found_post=[]
    for item in arr:
        if s.lower() in item.content.lower():
            found_post.append(item)
    return found_post
