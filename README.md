# Описание
Сервис представляет собой WhatsApp бота для управления напоминаниями. На текущий момент реализовано:
1. Создание напоминаний
2. Показ активных напоминаний
3. Удаление напоминания
4. Создание повторяющихся напомимнаний

Демонстрация работы: https://drive.google.com/file/d/1L2me2qgiuW-dTE7QEqDmhOBIgVOuplB3/view?usp=sharing

# Технологии
- Poetry
- FastAPI
- Uvicorn
- Docker
- Postgres
- SQLAlchemy
- Alembic
- Ngrok
- Twilio

# Установка
### Предварительно 
1. Получить `Twilio Auth Token` и `Twilio SID`. Для этого нужно зарегистрироваться на 
[twilio.com](https://www.twilio.com) и перейти на страницу 
[console](https://www.twilio.com/console). Они будут тут:

![image](https://github.com/pandenic/whatsapp_bot/assets/114985447/8ecd28dd-ed2f-45d7-9ff6-b88b5f00bb55)



3. Получить `Ngrok Auth Token`. Для этого нужно зарегистрироваться на [ngrok.com](https://ngrok.com/).
Затем перейти на [dashboard](https://dashboard.ngrok.com/get-started/your-authtoken). Он будет тут:

![image](https://github.com/pandenic/whatsapp_bot/assets/114985447/d747046c-3979-4065-a099-6a3bde349d80)



5. Установить ngrok: [инструкция](https://ngrok.com/docs/getting-started/).
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

8. Выполнить миграции:
```bash
alembic upgrade head
```

9. Запустить `uvicorn` сервер:
```bash
uvicorn src.main:app
```

10. Запустить `ngrok` в отдельной консоли в интерактивном режиме:
```bash
ngrok http 8000
```

11. Скопировать `endpoint` с [dashboard ngrok](https://dashboard.ngrok.com/cloud-edge/endpoints).
Он будет тут:

 ![image](https://github.com/pandenic/whatsapp_bot/assets/114985447/b360fa6b-eb59-4e06-9203-701e6b04e0e7)


13. Вставить его на [twilio](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn)
вкладке `sandbox settings` и добавить `/api/v1/bot/chat` в конце к `endpoint`. Вот так:

 ![image](https://github.com/pandenic/whatsapp_bot/assets/114985447/cb25d6dc-02b7-46e2-a486-556564a8e1a6)


Всё готово!

### Использование!


Для получения доступа к боту нужно отправить сообщение с кодом на номер: 
![image](https://github.com/pandenic/whatsapp_bot/assets/114985447/6620092c-1473-4964-90c8-ce7abc7fcebd)


__Команды для бота__

1. `Menu` - возврат в основное меню
   - `1` : `Create reminder` - создание неповторяющегося напоминания.
     - Создание напоминания: `HH:MM dd.mm.YYYY text`. 
       - `HH:MM` - время от 0:00 до 23:59. 
       - `dd.mm.YYYY` - дата от 01.01.1600 до 31.12.9999. 
       - `text` - текст напоминания.
   - `2` : `Show active reminders` - показать активные напоминания
   - `3` : `Delete reminder` - удалить выбранное напоминание
     - Удаление напоминания: ввести номер напоминания из списка ниже
   - `4` : `Create repeatable reminder` - создать повторяющееся напоминание
     - Создание повторяющегося напоминания: `[code] HH:MM dd.mm.YYYY text`. 
       - `[code]` - числовой год сценария повторения:
         - `0` : `Non-repeatable` - напоминание не повторяется
         - `1` : `Everyday` - напоминание повторяется каждый день
         - `2` : `Every week` - напоминание повторяется каждую неделю
         - `3` : `Every year` - напоминания повторяются каждый год
       - `HH:MM` - время от 0:00 до 23:59. 
       - `dd.mm.YYYY` - дата от 01.01.1600 до 31.12.9999. 
       - `text` - текст напоминания.


__Примеры__
---
Создание напоминания: 
```commandline
21:13 20.03.2024 drop table;
```

Ответ: 
```commandline
Reminder:
drop table;
saved.
You will be notified at:
2024-03-20 21:13:00.
```
---
Просмотр напоминаний:
```commandline
Your active reminders:

0: 2024-03-19 23:00:00 hello
1: 2024-05-19 23:00:00 hello
2: 2024-03-19 23:00:00 hello
3: 2024-12-19 23:00:00 hello
4: 2024-03-19 23:00:00 hello
5: 2024-03-19 23:00:00 hello
6: 2024-03-19 15:57:00 hello
7: 2024-09-02 15:57:00 hello
8: 2024-04-18 15:57:00 hello
9: 2024-03-18 15:57:00 hello
10: 2024-03-18 16:57:00 hello
11: 2024-03-19 16:57:00 hello
12: 2024-03-18 16:57:00 hello

```
---
Удаление напоминаний:
```commandline
Choose reminder to delete.
Just write a number.

Your active reminders:

0: 2024-03-19 23:00:00 hello
1: 2024-05-19 23:00:00 hello
2: 2024-03-19 23:00:00 hello
3: 2024-12-19 23:00:00 hello
4: 2024-03-19 23:00:00 hello
```
После выбора, например, 3го:
```commandline
Successfully deleted.

You're active reminders:

0: 2024-03-19 23:00:00 hello
1: 2024-05-19 23:00:00 hello
2: 2024-03-19 23:00:00 hello
3: 2024-03-19 23:00:00 hello
```
---
Создание повторяющихся напоминаний:
```commandline
You can choose a repetition by code:

0: Non-repeatable
1: Everyday
2: Every week
3: Every month
4: Every year

You can create a reminder using format:
[repeat_code] HH:MM dd.mm.YYYY any text
Example:
1 20:21 12.12.2025 drop table;
```
Ответ:
```commandline
Reminder:
drop table;
saved.
You will be notified at:
2025-12-12 21:21:00.

It will be repeated everyday
```


#  Что можно реализовать дополнительно:
- Изменение часового пояса
- Более сложную валидацию команд
- Выполнить рефакторинг: привести всё к классам, выделить повторяющийся код в отдельные функции, 
сократить перемешивание функций из разных модулей
- Добавить unittest'ы
- Прикрутить логгирование
- Добавить кастомные исключения
- Прикрутить redis или rabbitMQ для управления очередью нотификаций и сообщений
- Контейнеризировать всё
- Добавить валидацию телефонного номера
- Деплой и CI/CD
