from random import randint, choices
import itertools
import asyncio
import requests
from glom import glom
from faker import Faker
from config import Config


def post_json_client(url, data, headers={}):
    content_type = {'Content-type': 'application/json'}
    res = requests.post(Config.APPLICATION_URL + url, json=data, headers={**content_type, **headers})
    return res.json()


async def create_users_with_posts(data):
    userdata = post_json_client('api/accounts/signup/', data)
    token = post_json_client('api/accounts/signin/', {'username': data['username'], 'password': data['password']})

    posts = [{
            'title': fake.sentence()[:50],
            'body': fake.text()
        } for _ in range(randint(1, Config.MAX_POSTS_PER_USER))]

    fresh_posts = await asyncio.gather(
        *(create_post(post, token['token']) for post in posts),
    )

    return {**userdata, **token, **{'posts': fresh_posts}}


async def create_post(data, token):
    return post_json_client('api/posts/', data, headers={'Authorization': f'Bearer {token}'})


async def create_reaction(post_id, token):
    return post_json_client(f'api/posts/{post_id}/like/', {}, headers={'Authorization': f'Bearer {token}'})


if __name__ == '__main__':
    fake = Faker()
    users = [{
            'email': fake.email(),
            'username': fake.first_name().lower(),
            'password': fake.password()
        } for _ in range(Config.NUMBER_OF_USERS)]

    loop = asyncio.get_event_loop()

    users_posts = loop.run_until_complete(asyncio.gather(
        *(create_users_with_posts(user) for user in users),
    ))

    posts_ids = glom(users_posts, [('posts', ['id'])])
    posts_ids = list(itertools.chain(*posts_ids))
    tokens = glom(users_posts, ['token'])

    # generate post-token pairs
    post_token_pairs = []
    for token in tokens:
        for post_id in choices(posts_ids, k=randint(1, Config.MAX_LIKES_PER_USER)):
            post_token_pairs.append([post_id, token])

    reactions = loop.run_until_complete(asyncio.gather(
        *(create_reaction(*post_token) for post_token in post_token_pairs),
    ))

    loop.close()
