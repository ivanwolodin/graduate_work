import re
from typing import Union

from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat
from langchain_core.tools import tool
import json

PROMPT_FILM_COUNT = 30
PROMPT_FORMAT_DIRECTIVE = "!в формате json"
PROMPT_COUNT = 5
FILM_COUNT = 10
AUTH = "YjRiMWFhMTktZDNlYS00ZDk5LWFmZjQtMTRjMjU2ZmZlNmZkOjczYmQyMjY3LTkxMjktNDIzMS1hZGEzLTc4OWM1NWI5MTI2MQ=="


# @tool
def check_film(a: str) -> bool:
    """Проверяет, есть ли фильм с таким названием в АБВГД справочнике"""
    return a[0] not in 'А'


def check_answer(answer: str, count: int) -> Union[bool, str]:
    """Проверяет валидность Json, возвращает список существующих фильмов"""
    try:
        answer_json = json.loads(re.sub(r"\n", "", answer.content))

        valid_films = []
        for film in answer_json:
            if check_film(film.get('title')):
                valid_films.append(film.get('title'))

        return valid_films

    except ValueError:
        return False


# tools = [check_film]


giga = GigaChat(credentials=AUTH,
                model='GigaChat:latest',
                verify_ssl_certs=False
                )

llm_with_tools = giga.bind()
# llm = giga.bind()

def get_suggestion(like_films_prompt: list | str, user_description: str, additional_info: str = '') -> list:

    msgs = [SystemMessage(
        content='Ты рекомендательный сервис, отдавай рекомендуемый список в json формате,\
            со структурой где поле title - наименование фильма'
    ), HumanMessage(
        content=like_films_prompt + user_description + additional_info
        # content=f'Рекомендуй {PROMPT_FILM_COUNT} фильмов для пользователя {user_description} {additional_info}.\
        #     Ранее ему понравились фильмы: {", ".join(like_films)}. {PROMPT_FORMAT_DIRECTIVE}'
    )]

    # content=f'Рекомендуй {PROMPT_FILM_COUNT} фильмов для девочки 5 лет, в канун нового года. Ей нравятся фильмы: Звездные войны, Ну погоди, Винни Пух. {PROMPT_FORMAT_DIRECTIVE}'
    answer = giga(msgs)
    msgs.append(answer)

    films = []
    for _ in range(PROMPT_COUNT):
        check_result = check_answer(answer, FILM_COUNT)
        if check_result is False:
            msgs.append(HumanMessage(
                content=f'Исправь свой ответ на корректный JSON формат.'))
            answer = giga(msgs)
            msgs.append(answer)
        else:
            films += check_result
            if len(films) < FILM_COUNT:
                msgs.append(
                    HumanMessage(
                        content=f' Выведи еще список из {PROMPT_FILM_COUNT} рекомендуемых фильмов,\
                        фильмы из прошлого сообщения не выводи. {PROMPT_FORMAT_DIRECTIVE}'
                    )
                )
                answer = giga(msgs)
                msgs.append(answer)
            else:
                break

    return films
