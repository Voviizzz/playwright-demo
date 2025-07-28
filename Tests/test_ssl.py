# Данный тест для запуска в режиме без SSL, и для выбора нужного элемента из дубля элементов.



# from playwright.sync_api import Page
# import time
# class TestSSL:
#     def test_ssl(self, browser, page: Page):
#         context = browser.new_context(ignore_https_errors = True)
#         page = context.new_page()
#         page.goto("url_стенда")
#         page.reload()
#         locator1 = page.locator("//span[text()[contains(.,'материалы ')]]")
#         locator1.scroll_into_view_if_needed()
#         locator1.click()
#         full_text = locator1.text_content()
    
#     # Проверки
#         assert page.url == "url_стенда"
#         assert locator1.is_visible()
#         assert "информационных технологий и массовых коммуникаций" in full_text, "Текст отсутствует"
        
    
#     # Закрываем контекст
#         context.close()