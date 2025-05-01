document.addEventListener('DOMContentLoaded', function() {
    // Конфигурация видимых элементов для каждого типа вопроса
    const fieldGroups = {
        'TX': ['correct_answer', 'answer_fuzzy_match'],
        'TXA': ['correct_answer', 'answer_fuzzy_match'],
        'SN': ['answers-group'],
        'ML': ['answers-group']
    };

    // Функция для получения всех селекторов типа вопроса
    function getQuestionTypeSelects() {
        return Array.from(document.querySelectorAll('[id^="id_questions-"][id$="-question_type"]'));
    }

    // Функция для управления видимостью полей и инлайнов
    function updateFieldVisibility(questionTypeSelect) {
        const selectedType = questionTypeSelect.value;
        const inlineGroup = questionTypeSelect.closest('.inline-related');
        
        // 1. Управление обычными полями внутри этого инлайна
        Object.values(fieldGroups).flat().forEach(field => {
            const elements = inlineGroup.querySelectorAll(`.field-${field}, #${field}`);
            elements.forEach(el => el.style.display = 'none');
        });
        
        // 2. Управление инлайн-группой ответов
        const answerInlines = inlineGroup.querySelectorAll('.inline-related[id*="answers"]');
        
        if (selectedType === 'TX' || selectedType === 'TXA') {
            // Скрываем инлайны для текстовых вопросов
            answerInlines.forEach(inline => {
                inline.style.display = 'none';
            });
        } else {
            // Показываем инлайны для вопросов с выбором
            answerInlines.forEach(inline => {
                inline.style.display = 'block';
            });
        }
        
        // 3. Показываем нужные поля для текущего типа
        if (selectedType && fieldGroups[selectedType]) {
            fieldGroups[selectedType].forEach(field => {
                const elements = inlineGroup.querySelectorAll(`.field-${field}, #${field}`);
                elements.forEach(el => el.style.display = 'block');
            });
        }
    }

    // Инициализация обработчиков для всех существующих вопросов
    function initAllQuestionHandlers() {
        const questionTypeSelects = getQuestionTypeSelects();

        questionTypeSelects.forEach(select => {
            // Инициализация текущего состояния
            updateFieldVisibility(select);
            
            // Обработчик изменений
            select.addEventListener('change', function() {
                updateFieldVisibility(this);
            });
        });
    }

    // Обработчик для кнопки добавления нового вопроса
    function setupAddButton() {
        const addButton = document.querySelector('.add-handler.djn-add-handler.djn-model-quiz-question.djn-level-1');
        if (addButton) {
            addButton.addEventListener('click', function() {
                // Ждем пока Django добавит новый инлайн
                setTimeout(() => {
                    // Находим новый добавленный инлайн (последний в списке)
                    const allInlines = document.querySelectorAll('.last-related.djn-item.inline-related');
                    const newInline = allInlines[allInlines.length - 1];
                    
                    // Находим select типа вопроса в новом инлайне
                    const newSelect = newInline.querySelector('[id^="id_questions-"][id$="-question_type"]');
                    if (newSelect) {
                        // Инициализируем новый инлайн
                        updateFieldVisibility(newSelect);
                        
                        // Добавляем обработчик изменений
                        newSelect.addEventListener('change', function() {
                            updateFieldVisibility(this);
                        });
                    }
                }, 300); // Увеличено время ожидания для надежности
            });
        }
    }

    // Инициализация при загрузке страницы
    initAllQuestionHandlers();
    setupAddButton();

    // Дополнительно: обработчик для динамических изменений через MutationObserver
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.classList && node.classList.contains('djn-item')) {
                        const newSelect = node.querySelector('[id^="questions-"][id$="-type"]');
                        if (newSelect) {
                            updateFieldVisibility(newSelect);
                            newSelect.addEventListener('change', function() {
                                updateFieldVisibility(this);
                            });
                        }
                    }
                });
            }
        });
    });

    // Начинаем наблюдение за изменениями в контейнере инлайнов
    const container = document.querySelector('#questions-group');
    if (container) {
        observer.observe(container, {
            childList: true,
            subtree: true
        });
    }
});