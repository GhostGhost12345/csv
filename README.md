
В терминал:

pip install -r requirements.txt - зависимости

python main.py products.csv - без фильтрации или агрегации

python main.py products.csv --where "brand=xiaomi" - Фильтрация по тексту

python main.py products.csv --where "rating<4.7" - Фильтрация по рейтингу

python main.py products.csv --aggregate "price=avg" - среднее значение (агрегация)

python main.py products.csv --aggregate "rating=max" - максимальное значение (агрегация)

python main.py products.csv --aggregate "price=min" - минимальное значение