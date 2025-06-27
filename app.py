from flask import Flask, request, render_template, jsonify
import time  # Для имитации задержки расчёта
from IndividualsModelTest import calculate_risk_model
from CompaniesModelTest import calculate_risk_model_b

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/individual')
def individual():
    return render_template('form.html', user_type='individual')#, fields=individual_fields()

@app.route('/business')
def business():
    return render_template('form.html', user_type='business')#, fields=business_fields()

# def individual_fields():
#     #age, income, expenses, marital_status, dependents, has_property, has_car, employment_status,
#                    #months_since_last_delinquency, loan_purpose, loan_amount, loan_term
#     return ["Возраст", "Доход", "Кредитная история", "Семейное положение", "Трудовой стаж", "Образование", "Кол-во детей", "Имущество", "Расходы", "Сумма кредита", "Цель кредита", "Регион"]

# def business_fields():
#     return ["Годовой доход", "Активы", "Обязательства", "Оборот", "Чистая прибыль", "Стаж работы компании", "Сотрудники", "Кредиты", "Долги", "Сумма кредита", "Тип бизнеса", "Регион"]

@app.route('/calculate-loan-term', methods=['POST'])
def calculate_loan_term():
    data = request.json
    user_type = data.get("user_type")

    if user_type == "individual":
        min_term, max_term = calculate_loan_term_individual(data)
    elif user_type == "business":
        min_term, max_term = calculate_loan_term_business(data)
    else:
        raise ValueError("Неверный тип пользователя")

    return jsonify({"min": min_term, "max": max_term})

def calculate_loan_term_individual(data):
    base_min_term = 2  # Минимум 6 месяцев для физических лиц
    base_max_term = 260  # Максимум 60 месяцев для физических лиц

    income = float(data.get("income", 0))
    expenses = float(data.get("expenses", 0))
    loan_amount = float(data.get("loan_amount", 0))
    print(income, expenses, loan_amount)
    available_payment = (income - expenses) * 0.4  # Доступный платеж

    if income <= expenses:
        min_term = base_max_term  # Если доход меньше или равен расходам, минимальный срок
        max_term = base_max_term  # Максимальный срок - это базовый
    else:
        min_term = max(base_min_term, loan_amount / ((income - expenses) * 0.7) )  # Рассчитываем на основе суммы кредита
        max_term = min(base_max_term, loan_amount / ((income - expenses) * 0.1))
    # Гарантируем, что min_term <= max_ter
    if max_term-min_term<6:
        min_term = min(min_term, max_term)
        max_term+=6
    if min_term==0:
        min_term=1
    print(min_term, max_term)
    return round(min_term), round(max_term)

def calculate_loan_term_business(data):
    base_min_term = 2  # Минимум 12 месяцев
    base_max_term = 160  # Максимум 60 месяцев

    annual_turnover = float(data.get("annual_turnover", 0))
    loan_amount = float(data.get("loan_amount_business", 0))


    # Доля дохода, которую бизнес может отдавать на кредит (например, 20%)
    revenue_share_for_loan_min = 0.1
    revenue_share_for_loan_max = 0.5
    # Запас по сроку (например, в 2 раза больше минимального)
    term_multiplier = 2

    # Базовый срок (в месяцах)
    base_term_min = loan_amount / (annual_turnover * revenue_share_for_loan_max) * 12
    base_term_max = loan_amount / (annual_turnover * revenue_share_for_loan_min) * 12

    # Минимальный и максимальный сроки
    min_term = max(base_min_term, base_term_min)
    max_term = min(base_max_term, base_term_max)

    # Гарантируем, что min_term <= max_ter
    min_term = min(min_term, max_term)
    print(min_term, max_term)
    return round(min_term), round(max_term)




@app.route('/calculate-risk', methods=['POST'])
def calculate_risk():
    try:
        # Получаем данные как JSON
        data = request.get_json()
        if not data:
            return jsonify({"error": "Нет данных в запросе"}), 400  # Ошибка 400 - Неверный запрос

        print("Полученные данные:", data)  # Проверяем, что передаётся

        # Извлекаем значения с проверкой
        if 'age' in data:
            age = int(data.get('age', 0))
            income = float(data.get('income', 0))
            expenses = float(data.get('expenses', 0))
            marital_status = int(data.get('marital_status', 0))
            dependents = int(data.get('dependents', 0))
            has_property = int(data.get('has_property', 0))
            has_car = int(data.get('has_car', 0))
            employment_status = int(data.get('employment_status', 0))
            if data.get('months_since_last_delinquency') =='-':
                months_since_last_delinquency=999
            else:
                months_since_last_delinquency = int(data.get('months_since_last_delinquency', 0))
            loan_purpose = int(data.get('loan_purpose', 0))
            loan_amount = float(data.get('loan_amount', 0))
            loan_term = int(data.get('loan_term', 0))

            # Вызываем твою функцию расчёта риска
            risk = calculate_risk_model(age, income, expenses, marital_status, dependents, has_property, has_car, employment_status,
                       months_since_last_delinquency, loan_purpose, loan_amount, loan_term)
        else:
            print("+")
            legal_entity_type = int(data.get('legal_entity_type', 0))
            annual_revenue = float(data.get('annual_revenue', 0))
            total_assets = float(data.get('total_assets', 0))
            total_liabilities = float(data.get('total_liabilities', 0))
            annual_turnover = float(data.get('annual_turnover', 0))
            has_property = int(data.get('has_property_business', 0))
            total_loans = int(data.get('total_loans', 0))
            if data.get('months_since_last_delinquency_business')=="-":
                months_since_last_delinquency_business=999
            else:
                months_since_last_delinquency_business = int(data.get('months_since_last_delinquency_business', 0))
            loan_purpose_business = int(data.get('loan_purpose_business', 0))
            loan_amount_business = float(data.get('loan_amount_business', 0))
            loan_term = int(data.get('loan_term', 0))

            # Вызываем твою функцию расчёта риска
            risk = calculate_risk_model_b(legal_entity_type, annual_revenue, total_assets, total_liabilities, annual_turnover, has_property, total_loans,
                   months_since_last_delinquency_business, loan_purpose_business, loan_amount_business, loan_term)

        result = risk[0]  # если у тебя функция возвращает массив, берём первый элемент

        return jsonify({"risk": round(result * 100, 2)})

    except Exception as e:
        print("Ошибка при обработке запроса:", str(e))
        return jsonify({"error": "Ошибка сервера"}), 500


if __name__ == '__main__':
    app.run(debug=True)
