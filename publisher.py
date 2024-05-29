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