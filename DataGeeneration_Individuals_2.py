# import sqlite3
# #
# # Подключение к базе данных
# conn = sqlite3.connect('loan_risk.db')
# cursor = conn.cursor()
#
# # Выполнение удаления
# cursor.execute("""
#     DELETE FROM Individuals
# """)
#
# # Выполнение удаления
# cursor.execute("""
#     DELETE FROM Companies
# """)
# # Сохранение изменений
# conn.commit()
#
# # Проверка количества строк после удаления
# cursor.execute("SELECT COUNT(*) FROM Individuals")
# print("Осталось записей в Individuals:", cursor.fetchone()[0])
# cursor.execute("SELECT COUNT(*) FROM Companies")
# print("Осталось записей в Companies:", cursor.fetchone()[0])
#
# # Закрытие соединения
# conn.close()
#


import sqlite3
import random

# Подключение к базе данных
conn = sqlite3.connect('loan_risk.db')
cursor = conn.cursor()

# Константы
NUM_INDIVIDUALS = 500_000
BATCH_SIZE = 500  # Количество записей за раз

def calculate_loan_term(loan_amount, income, expenses):
    disposable_income = max(1000, income - expenses * 1.2)  # Чистый доход (не может быть < 1000), Учитываем непредвиденные расходы
    estimated_months = loan_amount / (max(disposable_income, 1000) / 5) # Грубо делим на 5 (чтобы был запас)
    return max(5, min(240, round(estimated_months)))


# Функция для изменения параметров в зависимости от дефолта
def adjust_parameters_for_default(age, income, expenses, marital_status, dependents, has_property, has_car, employment_status,
                                  months_since_last_delinquency, loan_purpose, loan_amount, loan_term, loan_default):
    if loan_default == 1:  # Дефолт
        # Увеличиваем расходы
        expenses *= random.uniform(1.2, 1.5)
        # Уменьшаем доход
        income *= random.uniform(0.7, 0.9)
        # Увеличиваем вероятность просрочек
        months_since_last_delinquency = random.randint(0, 6)
        # Увеличиваем количество иждивенцев
        dependents = min(5, dependents + random.randint(1, 2))
        # Увеличиваем вероятность отсутствия недвижимости и автомобиля
        has_property = 0 if random.random() < 0.9 else 1  # 80% вероятность отсутствия недвижимости
        has_car = 0 if random.random() < 0.9 else 1  # 80% вероятность отсутствия автомобиля
        # Увеличиваем срок кредита
        loan_term = min(120, loan_term + random.randint(12, 24))

        # Добавляем параметры, которые увеличивают риск дефолта
        age = random.choice([random.randint(18, 25), random.randint(51, 70)])  # Молодые или пожилые
        marital_status = 0 if random.random() < 0.9 else 1 # Холост/не замужем
        employment_status = random.choice([1, 2]) if random.random() < 0.9 else random.choice([0, 1, 2, 3]) # Безработный или самозанятый
        loan_purpose = random.choice([3, 4]) if random.random() < 0.9 else random.choice([0, 1, 2, 3, 4]) # Потребительский или рефинансирование
        loan_amount = min(loan_amount * 1.5, 10_000_000)  # Увеличиваем сумму кредита
    else:  # Нет дефолта
        # Уменьшаем расходы
        expenses *= random.uniform(0.7, 0.9)
        # Увеличиваем доход
        income *= random.uniform(1.1, 1.3)
        # Убираем просрочки
        months_since_last_delinquency = random.randint(12, 24)
        # Уменьшаем количество иждивенцев
        dependents = max(0, dependents - random.randint(0, 1))
        # Добавляем недвижимость и автомобиль
        has_property = 1 if random.random() < 0.9 else 0  # 80% вероятность наличия недвижимости
        has_car = 1 if random.random() < 0.9 else 0  # 80% вероятность наличия автомобиля
        # Уменьшаем срок кредита
        loan_term = max(12, loan_term - random.randint(6, 12))
        # Устанавливаем параметры, которые снижают риск дефолта
        age = random.randint(26, 50)  # Средний возраст
        marital_status = 1 if random.random() < 0.9 else 0  # Женат/замужем
        employment_status = 0 if random.random() < 0.9 else random.choice([0, 1, 2, 3]) # Наёмный работник
        loan_purpose = random.choice([0, 1]) if random.random() < 0.9 else random.choice([0, 1, 2, 3, 4])# Ипотека или автокредит
        loan_amount = max(15_000, loan_amount * 0.8)  # Уменьшаем сумму кредита

    return (age, income, expenses, marital_status, dependents, has_property, has_car, employment_status,
            months_since_last_delinquency, loan_purpose, loan_amount, loan_term, loan_default)
# Генерация данных для физических лиц (батчами)
individuals_data = []
for _ in range(NUM_INDIVIDUALS):
    # Генерация случайных параметров
    age = random.randint(18, 70)
    income = random.randint(15_000, 1_500_000)
    expenses = income * random.uniform(0.3, 1.5)  # Ограничение расходов (до 150% дохода)
    marital_status = random.choice([0, 1])
    dependents = random.randint(0, 5)
    has_property = random.choice([0, 1])
    has_car = random.choice([0, 1])
    employment_status = random.choice([0, 1, 2, 3])  # [0"Наём", 1"Безработный", 2"Самозанятый", 3"Предприниматель"]
    months_since_last_delinquency = random.randint(0, 24)
    loan_purpose = random.choice([0, 1, 2, 3, 4])  # [0"Ипотека", 1"Автокредит", 2"Образовательный", 3"Потребительский", 4"Рефинансирование"]
    loan_amount = random.randint(15_000, 10_000_000)
    loan_term = calculate_loan_term(loan_amount, income, expenses)  # Расчет срока кредита

    # Генерация дефолта (20% вероятность дефолта)
    loan_default = 1 if random.random() < 0.5 else 0

    # Корректировка параметров в зависимости от дефолта
    adjusted_data = adjust_parameters_for_default(age, income, expenses, marital_status, dependents, has_property, has_car,
                                                 employment_status, months_since_last_delinquency, loan_purpose, loan_amount,
                                                 loan_term, loan_default)

    individuals_data.append(adjusted_data)

    if len(individuals_data) >= BATCH_SIZE:
        cursor.executemany('''
            INSERT INTO Individuals (age, income, expenses, marital_status, dependents, has_property, has_car, employment_status,
                                     months_since_last_delinquency, loan_purpose, loan_amount, loan_term, loan_default)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', individuals_data)
        individuals_data = []  # Очистка списка после вставки

# Финальная вставка оставшихся данных
if individuals_data:
    cursor.executemany('''
        INSERT INTO Individuals (age, income, expenses, marital_status, dependents, has_property, has_car, employment_status,
                                 months_since_last_delinquency, loan_purpose, loan_amount, loan_term, loan_default)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', individuals_data)

# Сохранение изменений
conn.commit()
conn.close()

print("Данные для физических лиц успешно сгенерированы и записаны в базу.")

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Загрузка данных из базы
conn = sqlite3.connect('loan_risk.db')
df = pd.read_sql_query("SELECT * FROM Individuals", conn)
conn.close()

# Построение корреляционной матрицы
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title("Корреляционная матрица для физических лиц")
plt.show()