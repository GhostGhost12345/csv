
� ��������:

pip install -r requirements.txt - �����������

python main.py products.csv - ��� ���������� ��� ���������

python main.py products.csv --where "brand=xiaomi" - ���������� �� ������

python main.py products.csv --where "rating<4.7" - ���������� �� ��������

python main.py products.csv --aggregate "price=avg" - ������� �������� (���������)

python main.py products.csv --aggregate "rating=max" - ������������ �������� (���������)

python main.py products.csv --aggregate "price=min" - ����������� ��������