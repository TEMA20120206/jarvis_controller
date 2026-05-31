[app]

# НАЗВАНИЕ ВАШЕГО ПРИЛОЖЕНИЯ (будет под иконкой)
title = Jarvis Controller

# ВНУТРЕННЕЕ ИМЯ (только латиница, без пробелов)
package.name = jarvis

# УНИКАЛЬНЫЙ ИДЕНТИФИКАТОР (можно заменить на свое имя)
package.domain = org.jarvis

# ВЕРСИЯ
version = 1.0.0

# ГДЕ ЛЕЖИТ КОД
source.dir = .

# ГЛАВНЫЙ ФАЙЛ
main.py = main.py

# БИБЛИОТЕКИ, КОТОРЫЕ НУЖНЫ ВАШЕМУ ПРИЛОЖЕНИЮ
# kivy, requests и plyer установятся автоматически
requirements = python3,kivy,requests,plyer,kivymd

# РАЗРЕШЕНИЯ ДЛЯ ANDROID
android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE

android.api = 30
android.minapi = 21
android.targetapi = 30

# ФИКСИРУЕМ ВЕРСИЮ NDK, ЧТОБЫ ИЗБЕЖАТЬ ОШИБОК
android.ndk = 23c

# ГДЕ ЛЕЖИТ ИКОНКА (раскомментируйте, если есть)
icon.filename = %(source.dir)s/resources/icon.png

[buildozer]
log_level = 2
warn_on_root = 0