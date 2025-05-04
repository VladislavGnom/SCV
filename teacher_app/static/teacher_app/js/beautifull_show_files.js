document.getElementById('add-files-work-field').addEventListener('change', function(event) {
    const fileList = event.target.files; // Получаем список файлов
    const fileListElement = document.getElementById('file-list');
    fileListElement.innerHTML = ''; // Очищаем предыдущий список

    // Итерируемся по каждому загруженному файлу
    for (let i = 0; i < fileList.length; i++) {
        const file = fileList[i];
        const listItem = document.createElement('li'); // Создаем элемент списка
        listItem.className = 'li_file_item';
        listItem.textContent = `Файл: ${file.name}, Размер: ${(file.size / 1024).toFixed(2)} Кбайт`; // Заполняем информацию о файле
        fileListElement.appendChild(listItem); // Добавляем элемент списка в ul
    }
});