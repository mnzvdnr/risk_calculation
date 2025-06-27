import sqlite3

# Подключение к базе данных (или создание новой)
conn = sqlite3.connect('loan_risk.db')
cursor = conn.cursor()



# Создание таблицы для физических лиц
cursor.execute('''
CREATE TABLE IF NOT EXISTS Individuals (
    individual_id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER,
    income DECIMAL(15, 2),
    expenses DECIMAL(15, 2),
    marital_status BOOLEAN,
    dependents INTEGER,
    has_property INTEGER,
    has_car INTEGER,
    employment_status INTEGER,
    months_since_last_delinquency INTEGER,
    loan_purpose INTEGER,
    loan_amount DECIMAL(15, 2),
    loan_term INTEGER,
    loan_default BOOLEAN,
    FOREIGN KEY (employment_status) REFERENCES EmploymentStatuses(employment_status_id),
    FOREIGN KEY (loan_purpose) REFERENCES LoanPurposesIndividuals(loan_purpose_id)
);
''')

# Создание таблицы для юридических лиц
cursor.execute('''
CREATE TABLE IF NOT EXISTS Companies (
    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    legal_entity_type INTEGER,
    annual_revenue DECIMAL(15, 2),
    has_property BOOLEAN,
    total_assets DECIMAL(15, 2),
    total_liabilities DECIMAL(15, 2),
    annual_turnover DECIMAL(15, 2),
    total_loans INTEGER,
    months_since_last_delinquency INTEGER,
    loan_purpose INTEGER,
    loan_amount DECIMAL(15, 2),
    loan_term INTEGER,
    loan_default BOOLEAN,
    FOREIGN KEY (legal_entity_type) REFERENCES LegalEntityTypes(legal_entity_type_id),
    FOREIGN KEY (loan_purpose) REFERENCES LoanPurposesCompanies(loan_purpose_id)
);
''')

#employment_status [0"Наём", 1"Безработный", 2"Самозанятый", 3"Предприниматель"]
cursor.execute('''
CREATE TABLE IF NOT EXISTS EmploymentStatuses (
  employment_status_id INTEGER [primary key],
  status_name TEXT
 );
 ''')
cursor.executemany('''
INSERT INTO EmploymentStatuses (employment_status_id, status_name)
VALUES (?, ?)
''', [
    (0, "Наём"),
    (1, "Безработный"),
    (2, "Самозанятый"),
    (3, "Предприниматель")
])


#loan_purpose  # [0"Ипотека", 1"Автокредит", 2"Образовательный", 3"Потребительский", 4"Рефинансирование"]
cursor.execute('''
CREATE TABLE IF NOT EXISTS LoanPurposesIndividuals (
  loan_purpose_id INTEGER [primary key],
  purpose_name TEXT
 );
''')
cursor.executemany('''
INSERT INTO LoanPurposesIndividuals (loan_purpose_id, purpose_name)
VALUES (?, ?)
''', [
    (0, "Ипотека"),
    (1, "Автокредит"),
    (2, "Образовательный"),
    (3, "Потребительский"),
    (4, "Рефинансирование")
])


#legal_entity_type  [0"ООО", 1"АО", 2"ПАО", 3"НАО", 4"Производственный кооператив", 5"Хозяйственное товарищество", 6"ГУП", 7"МУП"]
cursor.execute('''
CREATE TABLE IF NOT EXISTS LegalEntityTypes (
  legal_entity_type_id INTEGER [primary key],
  type_name TEXT
);
''')
cursor.executemany('''
INSERT INTO LegalEntityTypes (legal_entity_type_id, type_name)
VALUES (?, ?)
''', [
    (0, "ООО"),
    (1, "АО"),
    (2, "ПАО"),
    (3, "НАО"),
    (4, "Производственный кооператив"),
    (5, "Хозяйственное товарищество"),
    (6, "ГУП"),
    (7, "МУП")
])



#loan_purpose  [0"Оборотный", 1"Инвестиционный", 2"Рефинансирование", 3"Недвижимость", 4"Лизинг", 5"Тендерный"]
cursor.execute('''
CREATE TABLE IF NOT EXISTS LoanPurposesCompanies (
  loan_purpose_id INTEGER [primary key],
  purpose_name TEXT
 );
''')
cursor.executemany('''
INSERT INTO LoanPurposesCompanies (loan_purpose_id, purpose_name)
VALUES (?, ?)
''', [
    (0, "Оборотный"),
    (1, "Инвестиционный"),
    (2, "Рефинансирование"),
    (3, "Недвижимость"),
    (4, "Лизинг"),
    (5, "Тендерный")
])

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()