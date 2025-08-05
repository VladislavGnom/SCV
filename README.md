# Educational Testing Platform - SCV

![Platform Logo](path/to/logo.png) *(Замечание: Здесь нужно вставить логотип платформы, если он есть)*

## О проекте

SCV - это веб-платформа для проверки знаний учащихся, разработанная на Django. Система предназначена для школьного образования и предоставляет удобные инструменты для проведения тестирования и анализа результатов.

## Основные возможности

### Для всех пользователей
- Приветственная страница с информацией о платформе
- Адаптивный слайдер (реализован с помощью GLide.js)

### Для учеников
- Личный кабинет с активными тестами
  <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/5a9bfa4e-a8fc-4c72-a588-951636bcf462" />
- Возможность загрузки решений (скриншотов)
  <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/437bc98a-0268-484c-83be-ab573fe41738" />
- Просмотр результатов выполненных тестов
  <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/e015a9b0-f7b4-443a-8283-b28758cc05fb" />
- Статистика успеваемости
  <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/a131a5ab-1459-4fa6-9da7-cd7c8a3e47f1" />
  <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/f1621a9d-91ab-4a33-9607-689a7582d288" />
- Личный профиль с основной информацией
  <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/2f98d128-2eec-496f-bc41-c5f0f6e809a1" />

### Для учителей
- Управление классами учащихся
- Создание и настройка тестов
- Добавление заданий в базу вопросов
  <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/a84dd636-4dcc-4678-8d7f-1a7f0b6c569d" />
  <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/7631635a-c909-4bce-9a37-f549ad5d3edf" />
- Просмотр результатов учащихся

### Для администраторов
- Полный контроль над системой через Django Admin
- Управление пользователями и правами доступа

## Технологии

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Дополнительные библиотеки**: GLide.js (для слайдера)

## Установка и запуск

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/yourusername/scv-platform.git
   ```

2. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Выполнить миграции:
   ```bash
   python manage.py migrate
   ```

4. Создать суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```

5. Запустить сервер:
   ```bash
   python manage.py runserver
   ```

## Скриншоты системы
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
  <div style="border: 1px solid #eee; padding: 15px; border-radius: 8px;">
    <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/a84dd636-4dcc-4678-8d7f-1a7f0b6c569d" />
  </div>
  <div style="border: 1px solid #eee; padding: 15px; border-radius: 8px;">
    <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/7631635a-c909-4bce-9a37-f549ad5d3edf" />
  </div>
  <div style="border: 1px solid #eee; padding: 15px; border-radius: 8px;">
    <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/12215704-712f-4901-a384-771d4341059d" />
  </div>
  <div style="border: 1px solid #eee; padding: 15px; border-radius: 8px;">
    <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/bd8cffc3-5132-448c-a8a5-955b9db7b26c" />
  </div>
  <div style="border: 1px solid #eee; padding: 15px; border-radius: 8px;">
    <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/61ed5fbd-c18a-4c5d-93ae-d6a88288ccb8" />
  </div>
  <div style="border: 1px solid #eee; padding: 15px; border-radius: 8px;">
    <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/b4f00827-3fba-426d-ba69-fd2e63240583" />
  </div>
  <div style="border: 1px solid #eee; padding: 15px; border-radius: 8px;">
    <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/57c053d1-1e3f-46cd-aa02-c04892109b30" />
  </div>
  <div style="border: 1px solid #eee; padding: 15px; border-radius: 8px;">
    <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/9f069495-c63e-4e2b-ad6c-89601d49c905" />
  </div>
  <div style="border: 1px solid #eee; padding: 15px; border-radius: 8px;">
    <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/fda6a4da-8293-4e35-85a0-3e193c794353" />
  </div>
  <div style="border: 1px solid #eee; padding: 15px; border-radius: 8px;">
    <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/5a9bfa4e-a8fc-4c72-a588-951636bcf462" />
  </div>
  <div style="border: 1px solid #eee; padding: 15px; border-radius: 8px;">
    <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/437bc98a-0268-484c-83be-ab573fe41738" />
  </div>
  <div style="border: 1px solid #eee; padding: 15px; border-radius: 8px;">
    <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/e015a9b0-f7b4-443a-8283-b28758cc05fb" />
  </div>
  <div style="border: 1px solid #eee; padding: 15px; border-radius: 8px;">
    <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/a131a5ab-1459-4fa6-9da7-cd7c8a3e47f1" />
  </div>
  <div style="border: 1px solid #eee; padding: 15px; border-radius: 8px;">
    <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/f1621a9d-91ab-4a33-9607-689a7582d288" />
  </div>
  <div style="border: 1px solid #eee; padding: 15px; border-radius: 8px;">
    <img width="257" height="354" alt="Image" src="https://github.com/user-attachments/assets/2f98d128-2eec-496f-bc41-c5f0f6e809a1" />
  </div>
</div>

## Дорожная карта

- [ ] Реализация страницы настроек пользователя
- [ ] Добавление системы уведомлений
- [ ] Рефакторинг кода

## Контакты

По вопросам сотрудничества и предложений обращайтесь:  
Email: vladfatov1054@gmail.com
Telegram: @Vladislav_5367
