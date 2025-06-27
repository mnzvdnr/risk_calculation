import sqlite3
import random

# Подключение к базе данных
conn = sqlite3.connect('loan_risk.db')
cursor = conn.cursor()

# Константы
NUM_COMPANIES = 500_000

BATCH_SIZE = 500  # Количество записей за раз

# Функция для изменения параметров в зависимости от дефолта
def adjust_parameters_for_default(legal_entity_type, annual_revenue, has_property, total_assets, total_liabilities,
                                  annual_turnover, total_loans, months_since_last_delinquency, loan_purpose, loan_amount,
                                  loan_term, loan_default):
    if loan_default == 1:  # Дефолт
        # Увеличиваем долговую нагрузку
        total_liabilities *= random.uniform(1.2, 1.5)
        # Уменьшаем выручку
        annual_revenue *= random.uniform(0.7, 0.9)
        # Уменьшаем оборот
        annual_turnover *= random.uniform(0.7, 0.9)
        # Уменьшаем активы
        total_assets *= random.uniform(0.7, 0.9)
        # Увеличиваем количество кредитов
        total_loans = min(10, total_loans + random.randint(1, 2))
        # Увеличиваем вероятность просрочек
        months_since_last_delinquency = random.randint(0, 6)
        # Убираем недвижимость
        has_property = 0 if random.random() < 0.9 else 1  # 90% вероятность отсутствия недвижимости
        # Увеличиваем срок кредита
        loan_term = min(240, loan_term + random.randint(12, 24))

        # Устанавливаем параметры, которые увеличивают риск дефолта
        legal_entity_type = random.choice([0, 1, 3, 4, 5])  # ООО, АО, НАО, Производственный кооператив, Хозяйственное товарищество
        loan_purpose = random.choice([1, 2, 4]) if random.random() < 0.9 else random.choice([0, 1, 2, 3, 4, 5])  # Инвестиционный, Рефинансирование, Лизинг
        loan_amount = min(loan_amount * 1.5, 500_000_000)  # Увеличиваем сумму кредита
    else:  # Нет дефолта
        # Уменьшаем долговую нагрузку
        total_liabilities *= random.uniform(0.7, 0.9)
        # Увеличиваем выручку
        annual_revenue *= random.uniform(1.1, 1.3)
        # Увеличиваем оборот
        annual_turnover *= random.uniform(1.1, 1.3)
        # Увеличиваем активы
        total_assets *= random.uniform(1.1, 1.3)
        # Уменьшаем количество кредитов
        total_loans = max(0, total_loans - random.randint(0, 1))
        # Убираем просрочки
        months_since_last_delinquency = random.randint(12, 36)
        # Добавляем недвижимость
        has_property = 1 if random.random() < 0.9 else 0  # 90% вероятность наличия недвижимости
        # Уменьшаем срок кредита
        loan_term = max(6, loan_term - random.randint(6, 12))

        # Устанавливаем параметры, которые снижают риск дефолта
        legal_entity_type = random.choice([2, 6, 7])  # ПАО, ГУП, МУП
        loan_purpose = random.choice([0, 3, 5]) if random.random() < 0.9 else random.choice([0, 1, 2, 3, 4, 5])  # Оборотный, Недвижимость, Тендерный
        loan_amount = max(500_000, loan_amount * 0.8)  # Уменьшаем сумму кредита

    return (legal_entity_type, annual_revenue, has_property, total_assets, total_liabilities,
            annual_turnover, total_loans, months_since_last_delinquency, loan_purpose, loan_amount,
            loan_term, loan_default)

# Функция для расчета срока кредита
def calculate_loan_term(loan_amount, annual_revenue):
    estimated_months = loan_amount / (max(annual_revenue / 12, 50_000) / 5)
    return max(6, min(240, round(estimated_months)))  # Ограничение 6–240 месяцев

# Генерация данных для юридических лиц (батчами)
companies_data = []
for _ in range(NUM_COMPANIES):
    # Генерация случайных параметров
    legal_entity_type = random.choice([0, 1, 2, 3, 4, 5, 6, 7])  # [0"ООО", 1"АО", 2"ПАО", 3"НАО", 4"Производственный кооператив", 5"Хозяйственное товарищество", 6"ГУП", 7"МУП"]
    annual_revenue = random.randint(1_000_000, 1_000_000_000)  # Годовая выручка
    total_assets = random.randint(500_000, 2_000_000_000)  # Общие активы
    total_liabilities = random.randint(100_000, 1_500_000_000)  # Общая задолженность
    annual_turnover = random.randint(100_000, annual_revenue)  # Оборот компании
    total_loans = random.randint(0, 10)  # Количество кредитов
    months_since_last_delinquency = random.randint(0, 36)  # Просрочки
    has_property = random.choice([0, 1])  # Наличие недвижимости
    loan_purpose = random.choice([0, 1, 2, 3, 4, 5])  # [0"Оборотный", 1"Инвестиционный", 2"Рефинансирование", 3"Недвижимость", 4"Лизинг", 5"Тендерный"]
    loan_amount = random.randint(500_000, 500_000_000)  # Сумма кредита
    loan_term = calculate_loan_term(loan_amount, annual_revenue)  # Расчет срока кредита

    # Генерация дефолта (20% вероятность дефолта)
    loan_default = 1 if random.random() < 0.5 else 0

    # Корректировка параметров в зависимости от дефолта
    adjusted_data = adjust_parameters_for_default(legal_entity_type, annual_revenue, has_property, total_assets, total_liabilities,
                                                 annual_turnover, total_loans, months_since_last_delinquency, loan_purpose, loan_amount,
                                                 loan_term, loan_default)

    companies_data.append(adjusted_data)

    if len(companies_data) >= BATCH_SIZE:
        cursor.executemany('''
            INSERT INTO Companies (legal_entity_type, annual_revenue, has_property, total_assets, total_liabilities,
                           annual_turnover, total_loans, months_since_last_delinquency, loan_purpose, loan_amount,
                           loan_term, loan_default)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', companies_data)
        companies_data = []  # Очистка списка после вставки

# Финальная вставка оставшихся данных
if companies_data:
    cursor.executemany('''
        INSERT INTO Companies (legal_entity_type, annual_revenue, has_property, total_assets, total_liabilities,
                           annual_turnover, total_loans, months_since_last_delinquency, loan_purpose, loan_amount,
                           loan_term, loan_default)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', companies_data)

# Сохранение изменений
conn.commit()
conn.close()

print("Данные для юридических лиц успешно сгенерированы и записаны в базу.")


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Загрузка данных из базы
conn = sqlite3.connect('loan_risk.db')
df = pd.read_sql_query("SELECT * FROM Companies", conn)
conn.close()

# Построение корреляционной матрицы
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title("Корреляционная матрица для физических лиц")
plt.show()