from flask import Flask, request, jsonify
import random

app = Flask(__name__)

riddles = {
    "easy": [
        {"question": "Что всегда идет, но никогда не приходит?", "answer": "Время"},
        {"question": "У кого есть руки, но нет рук?", "answer": "Часы"},
    ],
    "medium": [
        {"question": "Что растет, когда вы его убираете?", "answer": "Долги"},
        {"question": "Я легкий как перо, но даже самый сильный человек не может удержать меня долго. Что это?", "answer": "Дыхание"},
    ],
    "hard": [
        {"question": "Что можно увидеть только один раз в минуту, дважды в моменте, но ни разу в тысяче лет?", "answer": "Буква 'м'"},
        {"question": "Я всегда с тобой, но ты меня не видишь. Что это?", "answer": "Тень"},
    ]
}

@app.route('/post', methods=['POST'])
def post():
    req = request.json
    user_request = req['request']['command'].lower()
    session_attributes = req['session'].get('attributes', {})

    if 'level' not in session_attributes:
        session_attributes['level'] = None
        session_attributes['current_riddle'] = None
        session_attributes['correct_answers'] = 0
        session_attributes['wrong_answers'] = 0

    if 'выбрать уровень' in user_request:
        level = user_request.replace('выбрать уровень', '').strip()
        if level in riddles.keys():
            session_attributes['level'] = level