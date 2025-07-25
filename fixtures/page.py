import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
from playwright.sync_api import sync_playwright, Playwright
import os



def pytest_addoption(parser):
    """Пользовательские опции командной строки"""
    parser.addoption('--bn', action='store', default="chrome", help="Choose browser: chrome, remote_chrome or firefox")
    parser.addoption('--h', action='store', default=False, help='Choose headless: True or False')
    parser.addoption('--s', action='store', default={'width': 1920, 'height': 1080}, help='Size window: width,height')
    parser.addoption('--slow', action='store', default=200, help='Choose slow_mo for robot action')
    parser.addoption('--t', action='store', default=60000, help='Choose timeout')
    parser.addoption('--l', action='store', default='ru-RU', help='Choose locale')
    parser.addoption('--mobile', action="store", default=False, help="Run tests in mobile emulation mode")
    # parser.addini('qs_to_api_token', default=os.getenv("QASE_TOKEN"), help='Qase app token')



@pytest.fixture(scope='class')
def browser(request) -> Page:
    playwright = sync_playwright().start()
    browser_instance = None
    context = None
    
    try:
        # Мобильный режим (возвращает сразу контекст)
        if request.config.getoption("mobile"):
            context = mobile(playwright, request)  # mobile возвращает контекст
            page = context.new_page()
            yield page
            return  # Выходим раньше, чтобы избежать двойного закрытия
        
        # Десктопные режимы
        if request.config.getoption("bn") == 'remote_chrome':
            browser_instance = get_remote_chrome(playwright, request)
            context = get_context(browser_instance, request, 'remote')
        elif request.config.getoption("bn") == 'firefox':
            browser_instance = get_firefox_browser(playwright, request)
            context = get_context(browser_instance, request, 'local')
        elif request.config.getoption("bn") == 'chrome':
            browser_instance = get_chrome_browser(playwright, request)
            context = get_context(browser_instance, request, 'local')
        
        # Создаем страницу
        page = context.new_page()
        yield page
        
    finally:
        # Всегда закрываем ресурсы
        if context:
            context.close()
        if browser_instance:
            browser_instance.close()
        playwright.stop()


def get_firefox_browser(playwright, request) -> Browser:
    return playwright.firefox.launch(
        headless=request.config.getoption("h"),
        slow_mo=request.config.getoption("slow"),
    )
def mobile(playwright, request):
    # Пример конфигурации для мобильного устройства
    mobile_device = playwright.devices['iPhone 12']
    browser = playwright.chromium.launch(
        headless=request.config.getoption("h"),
        slow_mo=request.config.getoption("slow"),
    )
    context = browser.new_context(**mobile_device)
    return context

def get_chrome_browser(playwright, request) -> Browser:
    return playwright.chromium.launch(
        headless=request.config.getoption("h"),
        slow_mo=request.config.getoption("slow"),
        args=['--start-maximized']
    )

def get_remote_chrome(playwright, request) -> Browser:
    return playwright.chromium.launch(
        headless=True,
        slow_mo=request.config.getoption("slow")
    )

def get_context(browser, request, start) -> BrowserContext:
    if start == 'local':
        context = browser.new_context(
            no_viewport=True,
            locale=request.config.getoption('l')
        )
        context.set_default_timeout(
            timeout=request.config.getoption('t')
        )
        return context  # Обязательно возвращаем контекст!
    
    # Добавьте обработку других случаев
    elif start == 'remote':
        return browser.new_context(viewport={'width': 1920, 'height': 1080})
    
    # Всегда возвращайте контекст по умолчанию
    return browser.new_context()

@pytest.fixture(scope="function")
def return_back(browser):
    browser.go_back()

