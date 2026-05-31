[app]

title = Jarvis Controller
package.name = jarvis
package.domain = org.jarvis
version = 1.0.0
source.dir = .
main.py = main.py

requirements = python3,kivy,requests,plyer

android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE

android.api = 30
android.minapi = 21
android.targetapi = 30

android.ndk = 23c
android.sdk = 30

# Важно для GitHub Actions
android.accept_sdk_license = True

# Отключаем тесты для скорости
android.exclude_android_tests = True

# Если есть иконка
# icon.filename = %(source.dir)s/resources/icon.png

[buildozer]

log_level = 2
warn_on_root = 0
