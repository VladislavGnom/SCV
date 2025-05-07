document.getElementById('add-answers-field').addEventListener('change', function(event) {
    const file = event.target.files[0]; // Получаем первый загруженный файл
    const test_display_inputs = document.querySelectorAll('#add-title-input-tags-div .input-show-answer'); // Получаем все input внутри div
    let format_file = file.name.split('.').slice(-1);
    let is_true_format_file = (format_file == 'txt') ? true : false;

    if (file && is_true_format_file) {
        const reader = new FileReader(); // Создаем новый объект FileReader

        // Определяем обработчик события загрузки
        reader.onload = function(e) {
            const content = e.target.result; // Получаем содержимое файла
            const lines = content.split('\n'); // Разбиваем содержимое на строки
            
            // Итерируемся по строкам
            lines.forEach((line, index) => {
                try {
                    test_display_inputs[index].value = line;
                } catch (err) {
            
                } 
            });

            // Отображаем содержимое в элементе <pre>
            // document.getElementById('fileContent').textContent = content; // Отображаем содержимое в элементе <pre>
        };

        // Читаем файл как текст
        reader.readAsText(file);
    } else if (!is_true_format_file) {
        alert("Файл неверного формата.");
        console.log("Файл неверного формата.");
    } else {
        alert("Файл не выбран.");
        console.log("Файл не выбран.");
    }
});