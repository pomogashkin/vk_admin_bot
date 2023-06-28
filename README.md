# Бот Админ Вк

### Скрипт, который автоматически ведет страничку вк, заливая оригинальные посты раз в три часа.


### Чтобы развернуть проект на локальной машине нужно:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:pomogashkin/mailing_list.git
```

```
cd mailing_list
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Создать файл .env и вписать в него данные:

```
GROUP=АЙДИ ВАШЕЙ ГРУППЫ ИЛИ СТРАНИЦЫ (С МИНУСОМ, ЕСЛИ ГРУППА)
ALBUM_ID=АЙДИ АЛЬБОМА, В КОТОРЫЙ БУДУТ ДОБАВЛЯТЬСЯ КАРТИНКИ
ME=АЙДИ СТРАНИЦЫ С КОТОРОЙ БУДЕТ БРАТЬСЯ МУЗЫКА
LOGIN=ВАШ ТЕЛЕФОН ИЛИ ЛОГИН
PASSWORD=ПАРОЛЬ
URL=https://random-word-api.herokuapp.com/word
```

Запуск:

```
python main.py
```
