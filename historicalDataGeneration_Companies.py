import sqlite3
import random

# Подключение к базе данных
conn = sqlite3.connect('loan_risk.db')
cursor = conn.cursor()

# Константы
NUM_COMPANIES = 500_000
BATCH_SIZE = 500


# Функция для вычисления вероятности дефолта у юридического лица
def calculate_company_default(legal_entity_type, annual_revenue, has_property, total_assets, total_liabilities,
                           annual_turnover, total_loans, months_since_last_delinquency, loan_purpose, loan_amount,
                           loan_term):
    probability = 0.01  # Базовая вероятность 10%


    if total_liabilities / annual_revenue > 0.5:
        probability += 0.3  # Высокая долговая нагрузка
    if annual_turnover < annual_revenue * 0.3:
        probability += 0.25  # Очень низкий оборот
    if total_assets < total_liabilities:
        probability += 0.25  # Долгов больше, чем активов
    if loan_amount > annual_revenue * 2:
        probability += 0.25  # Кредит слишком большой относительно выручки
    if loan_term > 60:
        probability += 0.2  # Долгий срок кредита
    if loan_purpose in [1,2]:
        probability += 0.2  # Опасные цели кредита
    if total_loans > 3:
        probability += 0.15  # У компании уже много кредитов
    if months_since_last_delinquency< 5:
        probability += 0.35
    if has_property==0:
        probability += 0.15

    if legal_entity_type==2 or legal_entity_type==6 or legal_entity_type==7:
        probability -= 0.2



    probability = min(0.9, max(0.05, probability))  # Ограничиваем вероятность от 5% до 90%
    return random.random() < probability

# Функция для расчета срока кредита
def calculate_loan_term(loan_amount, annual_revenue):
    estimated_months = loan_amount / (max(annual_revenue / 12, 50000) / 5)
    return max(6, min(240, round(estimated_months)))  # Ограничение 1–20 лет


# Генерация данных для юридических лиц (батчами)
companies_data = []
for _ in range(NUM_COMPANIES):
    legal_entity_type = random.choice([0,1,2,3,4,5,6,7])#[0"ООО", 1"АО", 2"ПАО", 3"НАО",4"Производственный кооператив",5"Хозяйственное товарищество",6"ГУП", 7"МУП"]
    has_property = random.choice([0, 1])
    annual_revenue = random.randint(1_000_000, 1_000_000_000) # Годовая выручка
    total_assets = random.randint(500_000, 2_000_000_000) # Общие активы
    total_liabilities = random.randint(100_000, 1_500_000_000) # Общая задолженность
    annual_turnover = random.randint(100_000, annual_revenue) # Оборот компании
    total_loans = random.randint(0, 10)  # Количество кредитов
    months_since_last_delinquency = random.randint(0, 36)
    has_property = random.choice([0, 1]) #наличие недвижимости
    loan_purpose = random.choice([0,1,2,3,4,5]) #[0"Оборотный", 1"Инвестиционный", 2"Рефинансирование", 3"Недвижимость", 4"Лизинг", 5"Тендерный"]
    loan_amount = random.randint(500_000, 500_000_000) # Сумма кредита
    loan_term = calculate_loan_term(loan_amount, annual_revenue)  # Расчет срока кредита

    loan_default = calculate_company_default(legal_entity_type, annual_revenue, has_property, total_assets, total_liabilities,
                           annual_turnover, total_loans, months_since_last_delinquency, loan_purpose, loan_amount,
                           loan_term)

    companies_data.append((legal_entity_type, annual_revenue, has_property, total_assets, total_liabilities,
                           annual_turnover, total_loans, months_since_last_delinquency, loan_purpose, loan_amount,
                           loan_term, loan_default))

    if len(companies_data) >= BATCH_SIZE:
        cursor.executemany('''
            INSERT INTO Companies (legal_entity_type, annual_revenue, has_property, total_assets, total_liabilities,
                           annual_turnover, total_loans, months_since_last_delinquency, loan_purpose, loan_amount,
                           loan_term, loan_default)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', companies_data)
        companies_data = []

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

print("Данные о юридических лицах успешно сгенерированы и записаны в базу.")





# Подключение к базе данных
conn = sqlite3.connect('loan_risk.db')
cursor = conn.cursor()

# Выполнение запроса
cursor.execute("SELECT COUNT(*) FROM Companies WHERE loan_default = 1")

# Получение результата
count_defaults = cursor.fetchone()[0]
print("Количество дефолтов в Companies:", count_defaults)

cursor.execute("SELECT COUNT(*) FROM Companies")
count = cursor.fetchone()[0]
print("Количество дефолтов в Companies:", count)
# Закрытие соединения
conn.close()
