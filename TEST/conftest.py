import os          # для чтения переменных окружения
import pytest      # тестовый фреймворк
import requests    # HTTP-клиент для API
import allure      # для генерации отчетов Allure


# Фикстура: базовый URL для всех запросов
@pytest.fixture(scope="session")   # создаётся один раз на всю сессию тестов
def base_url() -> str:
    return os.getenv("BASE_URL", "http://localhost:3000")


# --- Allure helpers ---
class HttpSession(requests.Session):
    """Помогает автоматически прикреплять последние ответы в Allure"""
    def __init__(self):
        super().__init__()
        self.last_response = None
        
    def request(self, *args, **kwargs):
        resp = super().request(*args, **kwargs)
        self.last_response = resp
        return resp


@pytest.fixture(scope="session", autouse=True)
def allure_env(base_url):
    """Создаёт файл environment.properties, чтобы Allure показывал контекст тестов."""
    import pathlib
    results_dir = pathlib.Path("allure-results")
    results_dir.mkdir(parents=True, exist_ok=True)
    env_path = results_dir / "environment.properties"
    with env_path.open("w", encoding="utf-8") as f:
        f.write(f"BASE_URL={base_url}\n")
    yield


# Фикстура: HTTP-сессия (переиспользует соединения) с поддержкой Allure
@pytest.fixture(scope="session")
def http():
    s = HttpSession()
    s.headers.update({"Accept": "application/json"})  # JSON в ответах по умолчанию
    yield s                                          # объект сессии доступен в тестах
    s.close()                                        # корректное закрытие сессии


@pytest.fixture(autouse=True)
def _attach_last_response(request, http):
    """После каждого теста добавляет в Allure тело последнего ответа и метаинформацию."""
    yield
    resp = getattr(http, "last_response", None)
    if resp is not None:
        try:
            # Request line + URL
            req_line = f"{resp.request.method} {resp.url}\n"

            # Тело ответа (с обрезкой, если слишком длинное)
            body = resp.text
            if len(body) > 20000:
                body = body[:20000] + "\n... [truncated]"

            # Прикрепляем к отчёту
            allure.attach(
                req_line + body,
                name="last_response.txt",
                attachment_type=allure.attachment_type.TEXT
            )

            # Добавляем статус и заголовки
            meta = f"Status: {resp.status_code}\nHeaders: {dict(resp.headers)}"
            allure.attach(
                meta,
                name="response_meta.txt",
                attachment_type=allure.attachment_type.TEXT
            )
        except Exception as e:
            allure.attach(
                str(e),
                name="allure_attach_error.txt",
                attachment_type=allure.attachment_type.TEXT
            )