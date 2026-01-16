from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Основное меню
def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🗂 Создать файл"),
                KeyboardButton(text="🧪 Создать Pairwise тест")
            ],
            [
                KeyboardButton(text="🔍 Проверить API"),
                KeyboardButton(text="📑 Проверить JSON XML YAML")
            ],
            [
                KeyboardButton(text="📝 Создать документацию"),
                KeyboardButton(text="👥 Создать тестовые данные")
            ],
            [
                KeyboardButton(text="🕐 Конвертировать Timestamp"),
                KeyboardButton(text="🗃 Сгенерировать SQL")
            ],
            [
                KeyboardButton(text="Информация")
            ]
        ],
        resize_keyboard=True
    )

# Меню с кнопкой Назад
def get_back_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Назад в меню")]
        ],
        resize_keyboard=True
    )

# Текстовые сообщения
WELCOME_MSG = "Привет!👋 Я QA Ai Assistant 🤖\n\nВыбери, что нужно сделать:"
MENU_MSG = "Выбери, что нужно сделать:"
HELP_MSG = (
    "Доступные команды:\n"
    "/file - 🗂 Создать файл\n"
    "/pairwise - 🧪 Создать Pairwise тест\n"
    "/datavalidator - 📑 Валидатор данных JSON/XML/YAML\n"
    "/docs - 📝 Создать документацию (тест-кейс, чек-лист, баг-репорт)\n"
    "/testdata - 👥 Создать тестовые данные\n"
    "/timestamp - 🕐 Конвертировать Timestamp\n"
    "/sql - 🗃 Сгенерировать SQL\n"
    "/api - 🔍 Проверить API\n"
    "/cancel - отмена текущей операции\n"
    "/help - вызов справки\n\n"
    "ℹ️ Или используй кнопки меню ниже 👇"
)
