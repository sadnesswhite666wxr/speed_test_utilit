# Speedmeter CLI

Консольная утилита на Python для измерения скорости скачивания файлов по протоколу HTTP/HTTPS.

## Особенности

* **Анализ чистой скорости:** Использование прогревочного (Warm-up) запроса для исключения времени на DNS, TCP и TLS-рукопожатия из итоговой статистики.
* **Защита от кэширования:** Принудительное управление заголовками (`Cache-Control`, `Pragma`) для предотвращения отдачи файла из кэша CDN или сервера.
* **Надежность:** Обработка ошибок сети и статусов антибота (403 Forbidden).

## Требования

* Python 3.10+
* [Poetry](https://python-poetry.org/) (для управления зависимостями)

## Установка

1. Клонируйте репозиторий и установите зависимости:
```bash
git clone https://github.com/sadnesswhite666wxr/speed_test_utilit
cd speed_test_utilit
pip install poetry
poetry install
```

## Пример запуска

```bash
# Короткие флаги (-n и -u)
poetry run python main.py -n 10 -u https://www.hdwallpapers.in/download/beautiful_lake_landscape_scenery_4k_8k-HD.jpg

# Полные флаги (--count и --url)
poetry run python main.py --count 10 --url https://www.hdwallpapers.in/download/beautiful_lake_landscape_scenery_4k_8k-HD.jpg
```