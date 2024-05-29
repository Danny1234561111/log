## Логирование
Сначала я создал Main.py
Вначале я подключаю нужные библиотеки
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
import uvicorn
import os
import hashlib
app = FastAPI()
```
Потом я настраиваю логгер
```python
logger = logging.getLogger('user_actions')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('user_actions.log')
logger.addHandler(fh)
logger1 = logging.getLogger('user_actions1')
logger1.setLevel(logging.INFO)
fh = logging.FileHandler('user_actions1.log')
logger1.addHandler(fh)
```
Далее я осуществляю публикацию, а также подписку. В публикации, я получаю имя, пароль и сообщение, если аккаунт создан, то в логе я проверяю пароль, если нет, то я создаю аккаунт и публикую сообщение
В части Подписчика я просто вывожу последние логи.
```python
@app.post('/publish')
async def publish(request: Request):
    data = await request.json()
    user_id = data['user_id']
    password1 = data['password']
    action = data['action']
    with open('user_actions1.log', 'r') as f:
        lines = f.readlines()
    otvet=""
    for i in range(len(lines)):
        name, password = lines[i].split(':');
        if (name == user_id):
            otvet=password
    if (otvet==""):
        password=password1.encode('utf-8','replace')
        logger.info(f'{user_id}: {action}')
        logger1.info(f'{user_id}: {password}')
        return JSONResponse(content={"success": True})
    else:
        password=password[3:]
        password = password[:-2]
        password=bytes(password,'utf-8')
        new_key=password.decode('utf-8','replace')
        if new_key == password1:
            print('Пароль правильный')
            logger.info(f'{user_id}: {action}')
            return JSONResponse(content={"success": True})
        else:
            print('Пароль неправильный')
            return JSONResponse(content={"success": False})
@app.get('/subscribe')
async def subscribe():
    # Получить историю сообщений из лога
    with open('user_actions.log', 'r') as f:
        lines = f.readlines()

    # Преобразовать сообщения в список
    data = [line.strip() for line in lines]

    return JSONResponse(content={"messages": data})
```
Здесь я запускаю сервер через uvicorn
```python
if __name__ == "__main__":
    logger.info(f"Сервер запущен")
    uvicorn.run(app, host="0.0.0.0", port=8001)
```
А далее я просто описываю пример подписчика и отправителя
```python
import requests

# Отправить сообщение на сервер FastAPI
data = {'user_id': 'user5','password':"ppp", 'action': 'destroy the world'}
response = requests.post('http://localhost:8001/publish', json=data)
print(response)
# Проверить ответ от сервера
if response.status_code == 200:
    if (response.json()['success']==True):
        print('Сообщение успешно опубликовано')
    else:
        print('Пользователь существует, однако пароль неверный')
else:
    print('Ошибка при публикации сообщения')


import requests

# Получить сообщения с сервера Flask
response = requests.get('http://localhost:8001/subscribe')

# Проверить ответ от сервера
if response.status_code == 200:
    data = response.json()
    print('Последние сообщения:')
    for message in data['messages']:
        print(message)
else:
    print('Ошибка при получении сообщений')
```
