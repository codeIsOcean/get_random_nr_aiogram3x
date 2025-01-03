import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Количество попыток доступных пользователю в игре
ATTEMPTS = 5

# Словарь в котором будут храниться данные пользователя
user = {
    'in_game': False,
    'secret_number': None,
    'attempts': 0,
    'total_games': 0,
    'wins': 0
}


# Функция возвращающая случайное число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)


# Этот хэндлер будет срабатывать на команду /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
                         'Чтобы получить правила игры и список доступных '
                         'команд отправьте команду /help'
                         )


# Этот хэндлер будет срабатывать на команду '/help'
@dp.message(Command(commands='help'))
async def cmd_help(message: Message):
    await message.answer(
        'Правила игры: \n\nЯ загадываю число от 1 до 100,'
        f'Вам нужно его угадать \n У вас есть {ATTEMPTS}'
        f' попыток \n\nДоступные команды:\n/help - правила '
        'игры и список команд\n/cancel - выйти из игры\n'
        '/stat - посмотреть статистику\n\nДавай сыграем?'
    )


# Этот хэндлер будет срабатывать на команду '/stat'
@dp.message(Command(commands='stat'))
async def cmd_stat(message: Message):
    await message.answer(
        f'Всего игр сыграно: {user["total_games"]}\n'
        f'Игр выйграно: {user["wins"]}'
    )


# этот хендлер будет срабатывать на команду '/cancel'
@dp.message(Command(commands='cancel'))
async def cmd_cancel(message: Message):
    if user['in_game']:
        user['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом'
        )
    else:
        await message.answer(
            'А мы и так с вами не играем. '
            'Может, сыграем разок?'
        )


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра',
                                'играть', 'хочу играть']))
async def positive_answer(message: Message):
    if not user['in_game']:
        user['in_game'] = True
        user['secret_number'] = get_random_number()
        user['attempts'] = ATTEMPTS
        await message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100 '
            'попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать на число от 1 до 100 '
            'и команды /cancel и /stat'
        )


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def negative_answer(message: Message):
    if not user['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, число от 1 до 100'
        )


#  Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def number_asnwer(message: Message):
    if user['in_game']:
        if int(message.text) == user['secret_number']:
            user['in_game'] = False
            user['total_games'] += 1
            user['wins'] += 1
            await message.answer(
                'Ура!!! Вы угадали число! \n\n'
                'Может сыграем еще ?'
            )
        elif int(message.text) > user['secret_number']:
            user['attempts'] -= 1
            await message.answer(
                'Мое число меньше'
            )
        elif int(message.text) < user['secret_number']:
            user['attempts'] -= 1
            await message.answer(
                'Мое число большое'
            )

        if user['attempts'] == 0:
            user['in_game'] = False
            user['total_games'] += 1
            await message.answer(
                'К сожалению у Вас больше не осталось '
                'попыток. Вы проиграли : (\n\n Мое число '
                f'было {user['secret_number']}\n\nДавайте '
                'сыграем еще?'
            )
    else:
        await message.answer('Мы еще не играем. Хотите сыграть ?')


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message()
async def other_answers(message: Message):
    if user['in_game']:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?'
        )


if __name__ == '__main__':
    dp.run_polling(bot)
