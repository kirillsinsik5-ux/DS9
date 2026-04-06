# Установка библиотек:
# pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup

def get_python_news():
    """Загружает страницу python.org и выводит заголовки новостей"""
    try:
        # Загружаем страницу
        url = 'https://www.python.org/'
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Проверяем успешность запроса
        
        # Парсим HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ищем заголовки новостей (на сайте python.org новости обычно в ul с классом 'list-recent-events' или похожем)
        # Пробуем несколько селекторов
        news_items = []
        
        # Вариант 1: Блог посты на главной
        blog_posts = soup.select('.blog-widget li')
        if blog_posts:
            news_items = blog_posts
        else:
            # Вариант 2: События и новости
            news_items = soup.select('.list-recent-posts li')
        
        if not news_items:
            # Вариант 3: Попробуем найти другие новостные элементы
            news_items = soup.select('ul.menu li a')
        
        print("=" * 60)
        print("НОВОСТИ PYTHON.ORG")
        print("=" * 60)
        
        # Выводим нумерованный список заголовков
        count = 0
        for idx, item in enumerate(news_items[:10], 1):  # Берем первые 10 новостей
            title = item.get_text(strip=True)
            if title and len(title) > 3:  # Фильтруем пустые строки
                print(f"{idx}. {title}")
                count += 1
        
        if count == 0:
            print("Не удалось найти новости на странице")
            
    except requests.RequestException as e:
        print(f"Ошибка при загрузке страницы: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    get_python_news()