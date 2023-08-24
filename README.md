
# Portable Market

Open-source Telegram бот онлайн магазина для продажи виртуальных товаров с автоматизированной оплатой и ручной выдачей товаров с поддержкой кастомизации и полного спектра настроек.

## Особенности
1. Автоматическая оплата с проверкой с помощью платежной системы [AnyPay.io](https://anypay.io)
2. Неограниченное количество категорий товаров
3. Полная настройка и кастомизация товаров
4. Система скидок
5. Партнерская Система (реферальная)
6. Поддержка специальных чатов для информации о заказах
7. β: Внутренняя простая админ-панель
8. Система FAQ (вопрос-ответ)
9. Поддержка SQLite базы данных
10. Автоматическая система логирования с помощью библиотеки [loguru](https://github.com/Delgan/loguru)

## Установка
Для работы необходим Python 3.8+ (желательно 3.9+)

0. Установите все зависимые библиотеки с помощью консольной команды ``` pip install -r requirements.txt```
1. Настройте все необходимые поля в ```<корневая_папка>/bot/config.py```
2. Настройте платежную систему в ```<корневая_папка>/bot/handlers/admin/orders.py```
- Переменная ```api```, а также функции ```anypay_create_order``` и ```bad_order``` содержат поля, которые нужно настроить.
3. Настройте логи ([loguru](https://github.com/Delgan/loguru)) в ```<корневая папка>/bot/logs``` 
5. Запустите ```<корневая папка>/run.py```

## Настройка

- Доступ к базе данных с **товарами**, а также управление ими осуществляется с помощью ```<корневая папка>/bot/database/goods.db```
- Доступ к базе данных с **категориями** товаров, а также управление ими осуществляется с помощью ```<корневая папка>/bot/database/categories.db```
- Доступ к базе данных с **пользователями**, а также управление ими осуществляется с помощью ```<корневая папка>/bot/database/users.db```
- Доступ к базе данных с **заказами**, а также управление ими осуществляется с помощью ```<корневая папка>/bot/database/orders.db```
