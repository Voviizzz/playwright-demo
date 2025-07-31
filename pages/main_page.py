from pages.base import Base
from data.constants import Constants
from Locators.auth import Auth
from Locators.auth import LogAuth
from data.assertions import Assertions
from playwright.sync_api import Page
from data.environment import host
import os


class Main(Base):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.assertion = Assertions(page)

    def user_login(self):
        print("Starting login process...")
        self.open("")
    
    # Проверяем наличие полей ввода
        print(f"Using login: {os.getenv('AUTH_LOGIN')}")
        print(f"Using password: {os.getenv('AUTH_PASSWORD')}")
        
        username_field = self.page.locator(Auth.USERNAME_INPUT)
        password_field = self.page.locator(Auth.PASSWORD_INPUT)
        login_button = self.page.locator(Auth.LOGIN_BTN)
 
        print(f"Username field visible: {username_field.is_visible()}")
        print(f"Password field visible: {password_field.is_visible()}")
        print(f"Login button visible: {login_button.is_visible()}")
    
    # Заполняем поля
        username_field.fill(os.getenv("AUTH_LOGIN"))
        password_field.fill(os.getenv("AUTH_PASSWORD"))
    
    # Делаем скриншот перед нажатием кнопки
        self.page.screenshot(path="before_login.png")
    
    # Нажимаем кнопку входа
        login_button.click()
    
    # Делаем скриншот после нажатия
        self.page.screenshot(path="after_login.png")
    
    # Ждём либо перехода, либо сообщения об ошибке
        try:
            self.page.wait_for_url(
                f"{host.get_base_url()}inventory.html",
                timeout=30000
            )
            print("Login successful, on inventory page")
        except TimeoutError:
            error_msg = self.page.locator("h3[data-test='error']")
            if error_msg.is_visible():
                print(f"Login failed: {error_msg.inner_text()}")
            else:
                print("Unknown login error")
            self.page.screenshot(path="login_error.png")
            raise
    
        self.assertion.check_URL("inventory.html", "Wrong URL")
    