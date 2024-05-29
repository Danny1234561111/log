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
