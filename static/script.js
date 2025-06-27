document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("risk-form");
    const calculateRiskBtn = document.getElementById("calculate-risk");
    const calculateLoanBtn = document.getElementById("calculate-loan") ||
                           document.getElementById("calculate-loan-business");
    const loanTermSelect = document.getElementById("loan-term") ||
                          document.getElementById("loan-term-business");

    // Проверяем заполненность всех обязательных полей
    function checkFormValidity() {
        const requiredInputs = form.querySelectorAll("[required]");
        let allFilled = true;

        requiredInputs.forEach(input => {
            if (!input.value.trim()) {
                allFilled = false;
            }
        });

        // Управляем кнопкой "Рассчитать срок кредита"
        if (calculateLoanBtn) {
            calculateLoanBtn.disabled = !allFilled;
        }

        // Управляем кнопкой "Рассчитать риск"
        if (calculateRiskBtn) {
            calculateRiskBtn.disabled = !allFilled ||
                                      (loanTermSelect && loanTermSelect.value === "");
        }
    }

    // Вешаем обработчики на все поля формы
    form.addEventListener("input", checkFormValidity);


    // Дополнительно для селекта срока кредита
    if (loanTermSelect) {
        loanTermSelect.addEventListener("change", checkFormValidity);
    }

    // Первоначальная проверка
    checkFormValidity();
});


function switchUserType() {
    const userType = document.getElementById("user_type").value;
    window.location.href = userType === "individual" ? "/individual" : "/business";
}

function calculateLoanTerm(user_type) {
    let formData = { user_type: user_type };  // Начальный объект с типом пользователя

    // Заполнение данных в зависимости от типа пользователя
    if (user_type === "individual") {
        formData.income = document.getElementById('income').value;
        formData.expenses = document.getElementById('expenses').value;
        formData.loan_amount = document.getElementById('loan_amount').value;
    } else if (user_type === "business") {
        formData.annual_turnover = document.getElementById('annual_turnover').value;
        formData.loan_amount_business = document.getElementById('loan_amount_business').value;
    }

    fetch("/calculate-loan-term", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)  // Отправка данных в формате JSON
    })
    .then(response => response.json())
    .then(data => {
        const loanTermSelect = user_type === 'individual' ? document.getElementById("loan-term") : document.getElementById("loan-term-business");
        loanTermSelect.innerHTML = "";  // Очистить старые опции

        for (let i = data.min; i <= data.max; i += 6) {
            let option = document.createElement("option");
            option.value = i;
            option.textContent = `${i} месяцев`;  // Добавить месяц в текст
            loanTermSelect.appendChild(option);
        }

        loanTermSelect.disabled = false;  // Разблокировать выпадающий список
        loanTermSelect.value = data.min;  // Устанавливаем минимальный срок по умолчанию
    })
    .catch(error => {
        console.error('Error:', error);
    });
}




// Функция для получения данных формы
function getFormData() {
    const formData = {};
    document.querySelectorAll("#risk-form input, #risk-form select").forEach(input => {
        formData[input.name] = input.value;
    });
    return formData;
}



function goToHome() {
    window.location.href = "/";
}


function calculateRisk() {
    const formData = {};

    // Собираем данные со всех input, select и textarea внутри формы
    document.querySelectorAll("#risk-form input, #risk-form select, #risk-form textarea").forEach(element => {
        formData[element.name] = element.value;
    });

    // Добавляем значение срока кредита (для физических лиц или бизнеса)
    const loanTermSelect = document.getElementById("loan-term") || document.getElementById("loan-term-business");
    if (loanTermSelect && loanTermSelect.name) {
        formData[loanTermSelect.name] = loanTermSelect.value;
    }

    fetch("/calculate-risk", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error); // Показываем ошибку, если есть
            return;
        }

        const progressBar = document.getElementById("progress-bar");
        progressBar.style.width = "0%";
        let progress = 0;

        const interval = setInterval(() => {
            if (progress >= data.risk) {
                clearInterval(interval);
            } else {
                progress += 5;
                progressBar.style.width = `${progress}%`;
            }
        }, 100);

        document.getElementById("risk-result").textContent = `Риск выдачи займа: ${data.risk}%`;
        //////////////////////////////////////
        // Делаем все поля формы неактивными
        document.querySelectorAll("#risk-form input, #risk-form select, #risk-form textarea, #risk-form button").forEach(element => {
            if (element.id !== "go-home") {  // Можно исключить кнопку "Назад" или другую нужную
                element.disabled = true;
            }
        });




    })
    .catch(error => console.error("Ошибка при запросе:", error));
}


// Функция для разблокировки кнопки при заполнении всех полей
function checkFormCompletion() {
    let allFieldsFilled = true;

    document.querySelectorAll("#form-fields input").forEach(input => {
        if (input.value.trim() === "") {
            allFieldsFilled = false;
        }
    });

    document.getElementById("calculate-risk").disabled = !allFieldsFilled;
}

// Добавляем обработчик событий для отслеживания изменений в полях
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("#form-fields input").forEach(input => {
        input.addEventListener("input", checkFormCompletion);
    });
});


// Функция для разблокировки кнопки при заполнении всех полей
function checkFormCompletion() {
    let allFieldsFilled = true;

    document.querySelectorAll("#form-fields input").forEach(input => {
        if (input.value.trim() === "") {
            allFieldsFilled = false;
        }
    });

    document.getElementById("calculate-risk").disabled = !allFieldsFilled;
}

// Добавляем обработчик событий для отслеживания изменений в полях
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("#form-fields input").forEach(input => {
        input.addEventListener("input", checkFormCompletion);
    });




});






