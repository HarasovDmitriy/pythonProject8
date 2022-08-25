import json

from Class import User

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



def search_post(s: str, arr: list[User]) -> list[User]:
    '''Возвращает пост по поиску
    '''
    found_post=[]
    for item in arr:
        if s.lower() in item.content.lower():
            found_post.append(item)
    return found_post
