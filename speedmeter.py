import time
from typing import ClassVar
from urllib.parse import urlparse

from httpx import Client, HTTPStatusError, RequestError


class Speedmeter:
    DEFAULT_URL = "https://www.hdwallpapers.in/download/beautiful_lake_landscape_scenery_4k_8k-HD.jpg"
    TIMEOUT_SECONDS = 30
    HEADERS: ClassVar[dict[str, str]] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
    }
    DEFAULT_REQUEST_NUMBER = 10

    def __init__(
        self,
        request_number: int | None = DEFAULT_REQUEST_NUMBER,
        url: str | None = None,
    ) -> None:
        self.request_number = request_number or self.DEFAULT_REQUEST_NUMBER
        target_url = url or self.DEFAULT_URL
        self._validate_url(target_url)
        self.url = target_url

    @staticmethod
    def _validate_url(url: str) -> None:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValueError(
                f"Некорректный формат URL: '{url}'. Ссылка должна начинаться с http:// или https://"
            )

    def measure_speed(self) -> None:
        total_bytes = 0
        total_time = 0
        successful_requests = 0

        with Client(
            follow_redirects=True, timeout=self.TIMEOUT_SECONDS, headers=self.HEADERS
        ) as client:
            # Прогрев TCP/TLS соединения (не учитывается в итоговой статистике)
            print("Установление TLS-соединения...")

            if self._make_request(client) is None:
                print("Замеры невозможно произвести из-за ошибки сети")
                return

            for i in range(1, self.request_number + 1):
                result = self._make_request(client)
                if result is None:
                    print("Замеры невозможно произвести из за ошибки сети")
                    break

                data_len, request_time = result

                total_time += request_time
                total_bytes += data_len
                successful_requests += 1

                speed = (data_len * 8) / (request_time * 1_000_000)

                print(
                    f"Скорость: {speed:.2f} МБит/c "
                    f"Объем данных: {data_len / (1024 * 1024):.2f} МБ "
                    f"Время запроса: {request_time:.2f} с "
                    f"Источник: {self.url} "
                )

            if successful_requests > 0:
                self._show_total_report(
                    total_bytes=total_bytes,
                    total_time=total_time,
                    successful_requests=successful_requests,
                )

    @staticmethod
    def _show_total_report(
        total_bytes: int, total_time: float, successful_requests: int
    ) -> None:
        avg_time = total_time / successful_requests
        total_mb = total_bytes / (1024 * 1024)
        avg_speed_mbps = (total_bytes * 8) / (total_time * 1_000_000)
        avg_speed_mbytesps = total_mb / total_time

        print("\n" + 25 * "-")
        print(f"Общий объем скачанных данных: {total_mb:.2f} МБ")
        print(f"Общее время: {total_time:.2f} с")
        print(f"Среднее время: {avg_time:.2f} с")
        print(
            f"Средняя скорость: {avg_speed_mbytesps:.2f} МБ/c {avg_speed_mbps:.2f} Мбит/c"
        )
        print(25 * "-")

    def _make_request(self, client: Client) -> tuple[int, float] | None:
        start_time = time.perf_counter()
        try:
            response = client.get(self.url)
            response.raise_for_status()
        except HTTPStatusError as e:
            if e.response.status_code == 403:
                print("Не удалось пройти проверку антибот (403 Forbidden)")
            return None
        except RequestError:
            print(f"Не удалось соединиться с сервером: {self.url}")
            return None

        elapsed = time.perf_counter() - start_time
        data_len = len(response.content)

        return data_len, elapsed
