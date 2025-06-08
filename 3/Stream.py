import random
import time
from collections import deque

stocks = ['YNDX', 'SBER', 'GAZP']

# Очередь для хранения последних 5 цен по каждой акции
price_history = {stock: deque(maxlen=5) for stock in stocks}

# Начальные цены
current_prices = {stock: random.uniform(100, 200) for stock in stocks}

# Поток новых цен (генерация раз в 0.5 сек)
def stream_stock_prices():
    while True:
        stock = random.choice(stocks)
        # Имитация изменения цены на случайное значение
        change = random.uniform(-3, 3)
        new_price = round(current_prices[stock] + change, 2)
        current_prices[stock] = new_price
        yield stock, new_price
        time.sleep(0.5)

# Обработка потока
for stock, price in stream_stock_prices():
    price_history[stock].append(price)
    print(f"{stock}: новая цена {price} ₽, последние значения: {list(price_history[stock])}")

    # Если накопилось хотя бы 2 значения — считается динамика
    if len(price_history[stock]) >= 2:
        old_price = price_history[stock][0]
        new_price = price_history[stock][-1]
        delta = ((new_price - old_price) / old_price) * 100

        print(f"Изменение по {stock} за последние {len(price_history[stock])} обновлений: {delta:.2f}%")

        # Если скачок больше чем на 5% — выводится алерт
        if abs(delta) > 5:
            print(f"АЛЕРТ: цена {stock} изменилась на {delta:.2f}% за {len(price_history[stock])} обновлений!\n")