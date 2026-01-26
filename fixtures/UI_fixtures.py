import pytest

DEFAULT_UI_TIMEOUT = 30000  # Пример значения таймаута


@pytest.fixture(scope="session")  # Браузер запускается один раз для всей сессии
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)  # headless=True для CI/CD, headless=False для локальной разработки
    yield browser  # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    browser.close()  # Браузер закрывается после завершения всех тестов


@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)
    yield context
    #log_name = f"trace_{Tools.get_timestamp()}.zip"
    #trace_path = Tools.files_dir('playwright_trace', log_name)
    #context.tracing.stop(path=trace_path)
    #logging.info(f"ПУТЬ К ФАЙЛУ {trace_path}")#хуй пойми что добавили в доке где то блять работает где то нет, ебал я это
    context.close()


@pytest.fixture(scope="function")  # Страница создается для каждого теста
def page(context):
    page = context.new_page()
    yield page  # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    page.close()  # Страница закрывается после завершения теста