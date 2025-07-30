import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

def pytest_addoption(parser):
    """Пользовательские опции командной строки"""
    parser.addoption('--bn', action='store', default="chrome", help="Choose browser: chrome, remote_chrome or firefox")
    parser.addoption('--h', action='store', default="True", help='Choose headless: True or False')  # Исправлено на строку
    parser.addoption('--s', action='store', default="1920,1080", help='Size window: width,height')  # Исправлено на строку
    parser.addoption('--slow', action='store', default="200", help='Choose slow_mo for robot action')  # Исправлено на строку
    parser.addoption('--t', action='store', default="60000", help='Choose timeout')  # Исправлено на строку
    parser.addoption('--l', action='store', default='ru-RU', help='Choose locale')
    parser.addoption('--mobile', action="store_true", default=False, help="Run tests in mobile emulation mode")  # Исправлено на флаг

# Вспомогательные функции для преобразования опций
def get_bool_option(request, option_name):
    value = request.config.getoption(option_name)
    return value.lower() == 'true' if isinstance(value, str) else bool(value)

def get_int_option(request, option_name, default=0):
    try:
        return int(request.config.getoption(option_name))
    except (ValueError, TypeError):
        return default

def get_viewport_option(request):
    size_str = request.config.getoption("--s")
    try:
        width, height = map(int, size_str.split(','))
        return {"width": width, "height": height}
    except (ValueError, AttributeError):
        return {"width": 1920, "height": 1080}

@pytest.fixture(scope='class')
def browser(request) -> Page:
    playwright = sync_playwright().start()
    browser_instance = None
    context = None
    
    try:
        # Мобильный режим
        if request.config.getoption("--mobile"):
            context = mobile(playwright, request)
            page = context.new_page()
            yield page
            return
        
        # Десктопные режимы
        browser_name = request.config.getoption("--bn")
        
        if browser_name == 'remote_chrome':
            browser_instance = get_remote_chrome(playwright, request)
            context = get_context(browser_instance, request, 'remote')
        elif browser_name == 'firefox':
            browser_instance = get_firefox_browser(playwright, request)
            context = get_context(browser_instance, request, 'local')
        else:  # chrome по умолчанию
            browser_instance = get_chrome_browser(playwright, request)
            context = get_context(browser_instance, request, 'local')
        
        page = context.new_page()
        yield page
        
    finally:
        if context:
            context.close()
        if browser_instance:
            browser_instance.close()
        playwright.stop()

def get_firefox_browser(playwright, request) -> Browser:
    return playwright.firefox.launch(
        headless=get_bool_option(request, "--h"),
        slow_mo=get_int_option(request, "--slow", 200),
    )

def mobile(playwright, request):
    mobile_device = playwright.devices.get('iPhone 12', {})
    browser = playwright.chromium.launch(
        headless=get_bool_option(request, "--h"),
        slow_mo=get_int_option(request, "--slow", 200),
    )
    context = browser.new_context(**mobile_device)
    return context

def get_chrome_browser(playwright, request) -> Browser:
    return playwright.chromium.launch(
        headless=get_bool_option(request, "--h"),
        slow_mo=get_int_option(request, "--slow", 200),
        args=['--start-maximized']
    )

def get_remote_chrome(playwright, request) -> Browser:
    return playwright.chromium.launch(
        headless=True,
        slow_mo=get_int_option(request, "--slow", 200)
    )

def get_context(browser, request, start) -> BrowserContext:
    # Получаем таймаут
    timeout = get_int_option(request, "--t", 60000)
    
    if start == 'local':
        context = browser.new_context(
            no_viewport=True,
            locale=request.config.getoption("--l")
        )
        context.set_default_timeout(timeout=timeout)
        return context
    
    elif start == 'remote':
        viewport = get_viewport_option(request)
        return browser.new_context(viewport=viewport)
    
    return browser.new_context()

@pytest.fixture(scope="function")
def return_back(page: Page):
    page.go_back()
