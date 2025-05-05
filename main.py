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
        session_attributes['riddle_count'] = 0

    if 'выбрать уровень' in user_request:
        level = user_request.replace('выбрать уровень', '').strip()
        if level in riddles.keys():
            session_attributes['level'] = level
            session_attributes['current_riddle'] = random.choice(riddles[level])
            session_attributes['riddle_count'] += 1
            response_text = f"Вы выбрали уровень {level}. Загадка: {session_attributes['current_riddle']['question']} Какой ваш ответ?"
        else:
            response_text = "Пожалуйста, выберите уровень: легкий, средний или сложный."
    
    elif 'загадка' in user_request and session_attributes['level']:
        riddle = random.choice(riddles[session_attributes['level']])
        session_attributes['current_riddle'] = riddle
        session_attributes['riddle_count'] += 1
        response_text = f"Вот загадка: {riddle['question']}. Какой ваш ответ?"
    
    elif 'ответ' in user_request:
        answer = user_request.replace('ответ', '').strip()
        if answer.lower() == session_attributes['current_riddle']['answer'].lower():
            session_attributes['correct_answers'] += 1
            response_text = "Правильно! Молодец! Хотите еще загадку?"
        else:
            session_attributes['wrong_answers'] += 1
            response_text = f"Неправильно. Правильный ответ: {session_attributes['current_riddle']['answer']}. Хотите попробовать еще раз?"

    elif 'подсказка' in user_request and session_attributes['current_riddle']:
        hint = f"Первый символ ответа: {session_attributes['current_riddle']['answer'][0]}"
        response_text = f"Вот подсказка: {hint}"

    elif 'статистика' in user_request:
        correct = session_attributes['correct_answers']
        wrong = session_attributes['wrong_answers']
        total = session_attributes['riddle_count']
        response_text = f"Вы дали {correct} правильных ответов и {wrong} неправильных. Всего загадок: {total}."

    elif 'закончить' in user_request:
        response_text = "Спасибо за игру! Надеюсь, вам понравилось. До свидания!"
        session_attributes.clear()  # Очищаем атрибуты сессии

    else:
        response_text = "Скажите 'выбрать уровень', чтобы начать, или 'загадка', чтобы получить загадку."

    response = {
        "version": req['version'],
        "session": {
            "id": req['session']['id'],
            "message_id": req['session']['message_id'],
            "user_id": req['session']['user_id'],
            "attributes": session_attributes
        },
        "response": {"text": response_text,
            "end_session": False if 'закончить' not in user_request else True
        }
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5000)
