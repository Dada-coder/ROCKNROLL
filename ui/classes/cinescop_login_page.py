from playwright.sync_api import Page

class CinescopLoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://dev-cinescope.coconutqa.ru/login"

        # Локаторы элементов
        self.home_button = "a[href='/' and text()='Cinescope']"
        self.all_movies_button = "a[href='/movies' and text()='Все фильмы']"

        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"

        self.login_button = "button[type='submit']"
        self.register_button = "a[href='/register' and text()='Зарегистрироваться']"

    # Обработчики локаторов на шапке страницы
    def go_to_home_page(self):
        """Переход на главную страницу"""
        self.page.click(self.home_button)
        self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/")  # Ожидание загрузки главной страницы

    def go_to_all_movies(self):
        """Переход на страницу 'Все фильмы'"""
        self.page.click(self.all_movies_button)
        self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/movies")  # Ожидание загрузки страницы

    # Обработчики локаторов на теле страницы
    def open(self):
        """Переход на страницу входа"""
        self.page.goto(self.url)

    def enter_email(self, email: str):
        """Ввод email"""
        self.page.fill(self.email_input, email)

    def enter_password(self, password: str):
        """Ввод пароля"""
        self.page.fill(self.password_input, password)

    def click_login_button(self):
        """Клик по кнопке входа"""
        self.page.click(self.login_button)

    # Вспомогательные action методы
    def login(self, email: str, password: str):
        """Полный процесс входа"""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()

    def wait_redirect_to_home_page(self):
        """Ожидание перехода на домашнюю страницу"""
        self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/")  # Ожидание загрузки домашней страницы
        assert self.page.url == "https://dev-cinescope.coconutqa.ru/", "Редирект на домашнюю старницу не произошел"

    def check_allert(self):
        """Проверка всплывающего сообщения после редиректа"""
        # Проверка появления алерта с текстом "Вы вошли в аккаунт"
        notification_locator = self.page.get_by_text("Вы вошли в аккаунт")
        notification_locator.wait_for(state="visible")  # Ждем появления элемента
        assert notification_locator.is_visible(), "Уведомление не появилось"

        # Ожидание исчезновения алерта
        notification_locator.wait_for(state="hidden")  # Ждем, пока алерт исчезнет
        assert notification_locator.is_visible() == False, "Уведомление исчезло"
