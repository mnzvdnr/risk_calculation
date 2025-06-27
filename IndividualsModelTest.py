import pandas as pd
from autogluon.tabular import TabularPredictor

# Загрузка сохраненной модели
model_path = "AutogluonModels_Individuals"  # Укажи путь к модели \\ag-20250320_092044
predictor = TabularPredictor.load(model_path)












# Функция для расчёта рисков
def calculate_risk_model(age, income, expenses, marital_status, dependents, has_property, has_car, employment_status,
                   months_since_last_delinquency, loan_purpose, loan_amount, loan_term):
    # Создаем DataFrame для нового клиента
    new_data = pd.DataFrame([{
        "age": age,
        "income": income,
        "expenses": expenses,
        "marital_status": marital_status,
        "dependents": dependents,
        "has_property": has_property,
        "has_car": has_car,
        "employment_status": employment_status,
        "months_since_last_delinquency": months_since_last_delinquency,
        "loan_purpose": loan_purpose,
        "loan_amount": loan_amount,
        "loan_term": loan_term

    }])

    # Предсказание для нового клиента
    prediction = predictor.predict_proba(new_data).iloc[:, 1]


    return prediction


# # Пример использования функции
# age = 28
# income = 50_000
# expenses = 10_000
# marital_status = 1  # Женат/замужем
# dependents = 2
# has_property = 1  # Есть собственность
# has_car = 0  # Нет автомобиля
# employment_status = 0
# months_since_last_delinquency = 99
# loan_purpose = 1  # Цель займа
# loan_amount = 10_000  # Сумма займа
# loan_term = 7  # Срок займа (лет)
#
# # Расчет риска дефолта
# risk = calculate_risk_model(age, income, expenses, marital_status, dependents, has_property, has_car, employment_status,
#                       months_since_last_delinquency, loan_purpose, loan_amount, loan_term)
#
# print(f"Риск дефолта для данного клиента: {risk[0]:.4f}")

