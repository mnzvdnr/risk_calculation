import sqlite3
import pandas as pd
from autogluon.tabular import TabularPredictor

# Подключаемся к БД и загружаем данные
conn = sqlite3.connect('loan_risk.db')
query = "SELECT * FROM Companies"
df = pd.read_sql(query, conn)
conn.close()

# Убираем первичный ключ (он не нужен для обучения)
df.drop(columns=['company_id'], inplace=True)

# Определяем целевую переменную
target = 'loan_default'

# Разделяем на train и test
train_data = df.sample(frac=0.8, random_state=42)
test_data = df.drop(train_data.index)

hyperparameters = {
    'GBM': {},  # LightGBM
    'XGB': {},  # XGBoost
    'CAT': {},  # CatBoost
    'RF': {},  # Random Forest
    'LR': {},  # Логистическая регрессия
}


# Обучаем модель
predictor = TabularPredictor(label=target, problem_type='binary', path="AutogluonModels_Companies", eval_metric='roc_auc').fit(train_data, hyperparameters=hyperparameters)

# Делаем предсказания вероятностей на тестовом наборе
predictions = predictor.predict_proba(test_data)

print(predictions)



# Новые данные для предсказания
new_data = pd.DataFrame([{
    "legal_entity_type" : 0,
    "annual_revenue": 13_000_000,
    "has_property": 1,
    "total_assets": 45_000_000,
    "total_liabilities": 20_000_000,
    "annual_turnover": 56_000_000,
    "total_loans": 5,
    "months_since_last_delinquency": 4,
    "loan_purpose": 0,
    "loan_amount": 100_000_000,
    "loan_term": 24,
}])

# Предсказание вероятности дефолта
probability = predictor.predict_proba(new_data).iloc[:, 1]
print(f'Вероятность дефолта: {probability[0]:.4f}')


