from playwright.sync_api import sync_playwright
import time

# Создаем экземпляр Playwright и запускаем его
playwright = sync_playwright().start()

# Далее, используя объект playwright, можно запускать браузер и работать с ним
browser = playwright.chromium.launch(headless=False,slow_mo=35)
context = browser.new_context()
for i in range(20):
    a = context.new_page()
    a.goto("https://www.meme-arsenal.com/memes/0283b009e493ac72cfff44bc56fc1872.jpg")


#time.sleep(10)  # Сделаем sleep иначе браузер сразу закроектся перейдя к следующим строкам

# После выполнения необходимых действий, следует явно закрыть браузер
browser.close()

# И остановить Playwright, чтобы освободить ресурсы
playwright.stop()