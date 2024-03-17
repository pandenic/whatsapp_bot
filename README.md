# Описание
Сервис представляет собой WhatsApp бота для управления напоминаниями. На текущий момент реализовано:
1. Создание напоминаний

# Технологии
- Poetry
- FastAPI
- Uvicorn
- Docker
- Postgres
- SQLAlchemy
- Alembic
- Ngrok

# Установка
### Предварительно 
1. Получить `Twilio Auth Token` и `Twilio SID`. Для этого нужно зарегистрироваться на 
[twilio.com](https://www.twilio.com) и перейти на страницу 
[console](https://www.twilio.com/console). Они будут тут:
скриншот


2. Получить `Ngrok Auth Token`. Для этого нужно зарегистрироваться на [ngrok.com](https://ngrok.com/).
Затем перейти на [dashboard](https://dashboard.ngrok.com/get-started/your-authtoken). Он будет тут:
скриншот


3. Установить ngrok: [инструкция](https://ngrok.com/docs/getting-started/).
На Ubuntu:
```bash
sudo apt install ngrok
```
4. Привязать `Ngrok Auth Token`: [инструкция](https://ngrok.com/docs/getting-started/).
```bash
ngrok config add-authtoken <Ngrok Auth Token>
```

### Запуск
1. Склонировать репозиторий:
```bash
git clone git@github.com:pandenic/whatsapp_bot.git
```
2. Перейдите в каталог проекта:
```bash
cd whatsapp_bot
```
3. Установить `poetry`: [инструкция](https://python-poetry.org/docs/)
```bash
pip install poetry
```
4. Установить зависимости `poetry`:
```bash
poetry install --without dev
```
5. Запустить `poetry shell`:
```bash
poetry shell
```
6. Создать `.env` файл в корне проекта из `.env.example`. 
Заполнить`Twilio Auth Token` и `Twilio SID`,


7. Запустить `docker-compose.dev.yml`:
```bash
docker compose -f docker-compose.dev.yml up -d --build
```

8. Запустить `uvicorn` сервер:
```bash
uvicorn src.main:app
```

9. Запустить `ngrok` в отдельной консоли в интерактивном режиме:
```bash
ngrok http 8000
```

10. Скопировать `endpoint` с [dashboard ngrok](https://dashboard.ngrok.com/cloud-edge/endpoints).
Он будет тут: скриншот

11. Вставить его на [twilio](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn)
вкладке `sandbox settings` и добавить `/api/v1/bot/chat` в конце к `endpoint`. Вот так: скриншот

Всё готово!

### Использование

Для получения доступа к боту нужно отправить сообщение с кодом на номер: скриншот

__Команды для бота__
- Создание напоминания: `HH:MM dd.mm.YYYY text`. `HH:MM` - время от 0:00 до 23:59. 
`dd.mm.YYYY` - дата от 01.01.1600 до 31.12.9999. `text` - текст напоминания.


__Примеры__

Создание напоминания: 
```
21:13 20.03.2024 drop table;
```

Ответ: 
```
Reminder:
drop table;
saved.
You will be notified at:
2024-03-20 21:13:00.
```



#  Что можно реализовать дополнительно:
- Изменение часового пояса
- Более сложную валидацию команд
- Выполнить рефакторинг
- Добавить unittest'ы
- Прикрутить логгирование
- Добавить кастомные исключения
- Прикрутить redis или rabbitMQ для управления очередью нотификаций и сообщений
- Контейнеризировать всё
- Добавить валидацию телефонного номера
- Деплой и CI/CD