import sqlite3
import pandas as pd
from autogluon.tabular import TabularPredictor

# Подключаемся к БД и загружаем данные
conn = sqlite3.connect('loan_risk.db')
query = "SELECT * FROM Individuals"
df = pd.read_sql(query, conn)
conn.close()

# Убираем первичный ключ (он не нужен для обучения)
df.drop(columns=['individual_id'], inplace=True)

# Определяем целевую переменную
target = 'loan_default'

# Разделяем на train и test
train_data = df.sample(frac=0.8, random_state=42)
test_data = df.drop(train_data.index)

hyperparameters = {
    'GBM': {},  # LightGBM
    'XGB': {},  # XGBoost
    'CAT': {},  # CatBoost
    'NN_TORCH': {},  # Нейросеть
    'RF': {},  # Random Forest
    'LR': {},  # Логистическая регрессия
}

# Обучаем модель
predictor = TabularPredictor(label=target, problem_type='binary',  path="AutogluonModels_Individuals").fit(train_data, hyperparameters=hyperparameters) #, eval_metric='roc_auc'

# Делаем предсказания вероятностей на тестовом наборе
predictions = predictor.predict_proba(test_data)

print(predictions)

if input()=="+":
    predictor.save("IndividualsModel")

    print("Модель сохранена как 'IndividualsModel'")
else:
    print("Модель не сохранена")

# Новые данные для предсказания
new_data = pd.DataFrame([{
    "age": 18,
    "income": 0,
    "expenses": 30_000,
    "marital_status": 1,
    "dependents": 2,
    "has_property": 0,
    "has_car": 0,
    "employment_status": 0,
    "months_since_last_delinquency": 12,
    "loan_purpose": 4,
    "loan_amount": 100_0000,
    "loan_term": 7
}])

# Предсказание вероятности дефолта
probability = predictor.predict_proba(new_data).iloc[:, 1]
print(f'Вероятность дефолта: {probability[0]:.4f}')


