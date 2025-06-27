import pandas as pd
from autogluon.tabular import TabularPredictor

# Загрузка сохраненной модели
model_path = "AutogluonModels_Companies"  # Укажи путь к модели
predictor = TabularPredictor.load(model_path)


# Функция для расчёта рисков
def calculate_risk_model_b(legal_entity_type, annual_revenue, total_assets, total_liabilities, annual_turnover, has_property, total_loans,
                   months_since_last_delinquency, loan_purpose, loan_amount, loan_term):
    # Создаем DataFrame для нового клиента
    new_data = pd.DataFrame([{
        "legal_entity_type": legal_entity_type,
        "annual_revenue": annual_revenue,
        "has_property": has_property,
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "annual_turnover": annual_turnover,
        "total_loans": total_loans,
        "months_since_last_delinquency": months_since_last_delinquency,
        "loan_purpose": loan_purpose,
        "loan_amount": loan_amount,
        "loan_term": loan_term,
    }])

    # Предсказание для нового клиента
    prediction = predictor.predict_proba(new_data).iloc[:, 1]


    return prediction


# # Пример использования функции
# legal_entity_type = 2
# annual_revenue=1_000_000
# has_property=1
# total_assets=4_000_000
# total_liabilities=20_000_000
# annual_turnover=5_000_000
# total_loans = 2
# months_since_last_delinquency= 99
# loan_purpose= 0
# loan_amount=1_000_000
# loan_term=4
#
# # Расчет риска дефолта
# risk = calculate_risk_model_b(legal_entity_type, annual_revenue, total_assets, total_liabilities, annual_turnover, has_property, total_loans,
#                    months_since_last_delinquency, loan_purpose, loan_amount, loan_term)
#
# print(f"Риск дефолта для данного клиента: {risk[0]:.4f}")

