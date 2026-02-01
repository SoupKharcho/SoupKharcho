import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import re

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
BOT_TOKEN = '8362418376:AAH-gftEM32ZrZpGWmKNZY7BnI_g6ssquqE'
bot = telebot.TeleBot(BOT_TOKEN)

# Создаем клавиатуру
def create_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    
    # Первый ряд
    keyboard.add('7', '8', '9', '/')
    
    # Второй ряд
    keyboard.add('4', '5', '6', '*')
    
    # Третий ряд
    keyboard.add('1', '2', '3', '-')
    
    # Четвертый ряд
    keyboard.add('0', '.', '=', '+')
    
    # Дополнительные кнопки
    keyboard.add('C', '⌫', '(', ')')
    
    return keyboard

# Функция для вычисления выражения
def calculate_expression(expression):
    try:
        # Заменяем символы для безопасного вычисления
        expression = expression.replace('×', '*').replace('÷', '/')
        
        # Проверяем на безопасность (только цифры, операторы и скобки)
        if not re.match(r'^[\d\+\-\*\/\.\(\)\s]+$', expression.replace(' ', '')):
            return "Ошибка: Недопустимые символы"
        
        # Вычисляем результат
        result = eval(expression)
        
        # Округляем если нужно
        if isinstance(result, float) and result.is_integer():
            result = int(result)
            
        return str(result)
    
    except ZeroDivisionError:
        return "Ошибка: Деление на ноль"
    except SyntaxError:
        return "Ошибка: Неправильное выражение"
    except Exception as e:
        return f"Ошибка: {str(e)}"

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """🤖 *Калькулятор-бот*
    
Просто введите математическое выражение или используйте клавиатуру ниже.

Примеры:
• `2+2`
• `(5*3)/2`
• `10-4.5`

Используйте /help для справки"""
    
    bot.send_message(message.chat.id, welcome_text, 
                     parse_mode='Markdown', 
                     reply_markup=create_keyboard())

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """📚 *Справка по калькулятору*

Поддерживаемые операции:
• Сложение: `+`
• Вычитание: `-`
• Умножение: `*`
• Деление: `/`
• Скобки: `( )`

Примеры выражений:
• `2 + 3 * 4`
• `(15 + 5) / 4`
• `3.14 * 2`

Кнопки:
• `C` - Очистить
• `⌫` - Удалить последний символ
• `=` - Посчитать результат

Просто напишите выражение и бот его посчитает!"""
    
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip()
    
    # Очистить
    if text == 'C':
        bot.send_message(message.chat.id, "Очищено! Введите новое выражение.")
        return
    
    # Удалить последний символ (не реализовано полностью в этом примере)
    elif text == '⌫':
        bot.send_message(message.chat.id, "Для удаления просто отправьте выражение без последнего символа")
        return
    
    # Посчитать
    elif text == '=':
        bot.send_message(message.chat.id, "Введите выражение и затем нажмите = или отправьте его сразу")
        return
    
    # Если сообщение содержит математические операторы или цифры
    elif any(char.isdigit() or char in '+-*/.()' for char in text):
        # Проверяем, заканчивается ли на = или содержит =
        if text.endswith('='):
            expression = text[:-1]
        else:
            expression = text
        
        result = calculate_expression(expression)
        bot.send_message(message.chat.id, f"*Выражение:* `{expression}`\n*Результат:* `{result}`", 
                         parse_mode='Markdown')
    
    else:
        bot.send_message(message.chat.id, 
                         "Введите математическое выражение или используйте клавиатуру", 
                         reply_markup=create_keyboard())

# Запуск бота
if __name__ == '__main__':
    print("Бот калькулятор запущен...")
    bot.infinity_polling()
