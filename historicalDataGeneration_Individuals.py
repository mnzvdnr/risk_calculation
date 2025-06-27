import sqlite3
import random

# Подключение к базе данных
conn = sqlite3.connect('loan_risk.db')
cursor = conn.cursor()

# Константы
NUM_INDIVIDUALS = 400_000
BATCH_SIZE = 500  # Количество записей за раз


# Функция для вычисления вероятности дефолта у физического лица
def calculate_individual_default(income, expenses, marital_status, dependents, has_property, has_car, employment_status,
                                 months_since_last_delinquency, loan_purpose, loan_amount, loan_term):
    probability = 0.01  # Базовая вероятность 1%

    if (income - expenses) * 0.5 < (loan_amount / max(loan_term, 1)):
        probability += 0.3
    if (income - expenses)* 0.2 > (loan_amount / max(loan_term, 1)):
        probability -= 0.2
    if dependents > 3:
        probability += 0.1
    if has_property == 0:
        probability += 0.15
    if has_car == 0:
        probability += 0.1
    if marital_status == 0:
        probability += 0.15
    if months_since_last_delinquency < 5:
        probability += 0.25
    if loan_term > 60 and (employment_status == 2 or employment_status == 3):
        probability += 0.1
    if employment_status == 1:
        probability += 0.3
    if loan_purpose == 4:
        probability += 0.2


    probability = min(0.9, max(0.05, probability))  # Ограничиваем вероятность от 5% до 90%

    return random.random() < probability  # Если случайное число < probability, то дефолт (True)


# Функция для расчета срока кредита
def calculate_loan_term(loan_amount, income, expenses):
    disposable_income = max(1000, income - expenses * 1.2)  # Чистый доход (не может быть < 1000), Учитываем непредвиденные расходы
    estimated_months = loan_amount / (max(disposable_income, 1000) / 5) # Грубо делим на 5 (чтобы был запас)
    return max(5, min(240, round(estimated_months)))


# Генерация данных для физических лиц (батчами)
individuals_data = []
for _ in range(NUM_INDIVIDUALS):
    age = random.randint(18, 70)
    income = random.randint(15000, 1500000)
    expenses = income * random.uniform(0.3, 1.5)  # Ограничение расходов (до 150% дохода)
    marital_status = random.choice([0, 1])
    dependents = random.randint(0, 5)
    has_property = random.choice([0, 1])
    has_car = random.choice([0, 1])
    employment_status = random.choice([0,1,2,3]) #[0"Наём", 1"Безработный", 2"Самозанятый", 3"Предприниматель"]
    months_since_last_delinquency = random.randint(0, 24)
    loan_purpose = random.choice([0,1,2,3,4])#[0"Ипотека", 1"Автокредит", 2"Образовательный", 3"Потребительский", 4"Рефинансирование"]
    loan_amount = random.randint(15000, 10000000)

    loan_term = calculate_loan_term(loan_amount, income, expenses)  # Расчет срока кредита
    loan_default = calculate_individual_default(income, expenses, marital_status, dependents, has_property, has_car,
                                                employment_status,
                                                months_since_last_delinquency, loan_purpose, loan_amount, loan_term)

    individuals_data.append(
        (age, income, expenses, marital_status, dependents, has_property, has_car, employment_status,
         months_since_last_delinquency, loan_purpose, loan_amount, loan_term, loan_default))

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

print("Данные успешно сгенерированы и записаны в базу.")



# Подключение к базе данных
conn = sqlite3.connect('loan_risk.db')
cursor = conn.cursor()

# Выполнение запроса
cursor.execute("SELECT COUNT(*) FROM Individuals WHERE loan_default = 1")

# Получение результата
count_defaults = cursor.fetchone()[0]
print("Количество дефолтов в Individuals:", count_defaults)

cursor.execute("SELECT COUNT(*) FROM Individuals")
count = cursor.fetchone()[0]
print("Количество дефолтов в Individuals:", count)
# Закрытие соединения
conn.close()


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
