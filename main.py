import argparse

from speedmeter import Speedmeter


def main():
    parser = argparse.ArgumentParser(
        description="Утилита для замера скорости скачивания файлов из интернета."
    )
    parser.add_argument("-u", "--url", type=str, help="URL картинки в интернете")
    parser.add_argument(
        "-n", "--count", type=int, help="Количество запросов (по умолчанию: 10)."
    )

    args = parser.parse_args()

    speed_obj = Speedmeter(request_number=args.count, url=args.url)
    speed_obj.measure_speed()


if __name__ == "__main__":
    main()
