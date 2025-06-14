from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
import logging

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN,
          parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

async def set_default_commands(bot: Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand('start', 'Запустить бота'),
            BotCommand('manager', 'Чат с менеджером'),
            BotCommand('help', 'Техническая поддержка'),
            BotCommand('contacts', 'Контактная информация')
        ],
        scope=BotCommandScopeDefault()
    )

@dp.message_handler(commands='start')
async def command_start(message: types.Message):
    await message.reply(f'Доброго времени суток, {message.from_user.first_name}!',
                        reply_markup=kb)
    await set_default_commands(bot)

@dp.message_handler(commands='manager')
async def command_manager(message: types.Message):
    await message.reply('Если у Вас возникли вопросы, Вы можете задать их нашему менеджеру!',
                        reply_markup=manager_kb())

@dp.message_handler(commands='help')
async def command_manager(message: types.Message):
    await message.reply('Если у Вас возникли технические вопросы, связанные с работой нашего бота или разработкой Вашего, '
                        'то Вы можете написать нам, мы решим Вашу проблему!',
                        reply_markup=help_kb())

@dp.message_handler(commands='contacts')
async def command_manager(message: types.Message):
    await message.reply(text_contacts,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=manager_kb())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton('О нас 📃')).insert(KeyboardButton('Наши услуги 🚀')).add(KeyboardButton('Контактная информация 📱📩'))

photo_logo = 'https://t.me/forbot_nikita/2'

@dp.message_handler(text='О нас 📃')
async def description(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id,
                         photo=photo_logo,
                         caption=text_logo,
                         reply_markup=content,
                         parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(text='⬅️Назад')
async def chat(message: types.Message):
    await message.reply('Вы вернулись назад', reply_markup=kb)



def manager_kb():
    kb = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(text="Чат с менеджером", callback_data='manager', url='http://t.me/manager_fullstart')
    kb.add(btn)
    return kb

def help_kb():
    kb = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(text="Чат с тех.поддержкой", callback_data='helpi', url='http://t.me/nikitasyukhin')
    kb.add(btn)
    return kb


content = InlineKeyboardMarkup()
kb1 = InlineKeyboardMarkup()
btn1 = InlineKeyboardButton(text='Наше VK-сообщество', url='https://vk.com/full_start', callback_data='vk')
btn2 = InlineKeyboardButton(text='Наш YouTube-канал', url='https://www.youtube.com/channel/UCM46GXULmK-NLi7SemJ1XYQ', callback_data='yt')
btn3 = InlineKeyboardButton(text='Наш Telegram-канал', url='http://t.me/full_start', callback_data='tg')
content.add(btn1).add(btn2).add(btn3)


@dp.message_handler(text='Контактная информация 📱📩')
async def chat(message: types.Message):
    await message.reply(text=text_contacts,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=manager_kb())

@dp.message_handler(text='Наши услуги 🚀')
async def price(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Акции и скидки ⚡').add("⬅️Назад")
    await bot.send_message(message.chat.id, 'Перейдём к услугам✅', reply_markup=markup)
    btn_1 = (types.InlineKeyboardButton(text='Разработка Telegram-ботов', callback_data='main'))
    btn_2 = (types.InlineKeyboardButton(text='Курсы по программированию', callback_data='courses'))
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(btn_1).add(btn_2)
    await bot.send_message(chat_id=message.chat.id,
                           text=text_price,
                           parse_mode=ParseMode.MARKDOWN,
                           reply_markup=keyboard)

@dp.message_handler(text='Акции и скидки ⚡')
async def chat(message: types.Message):
    await message.reply(text=text_sales,
                        parse_mode=ParseMode.MARKDOWN)


@dp.callback_query_handler(text=['main', 'courses'])
async def first_btn_process(call: types.CallbackQuery):
    if call.data == 'main':
        await call.message.answer(text="*Выберите тариф*, по которому Вы хотели бы заказать разработку Telegram-бота:",
                                  parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=price1_main_kb())
    else:
        await call.message.answer(text="*Выберите курс*, который Вы хотели бы пройти:",
                                  parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=price1_courses_kb)

def price1_main_kb():
    kb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text='"LITE"', callback_data='lite')
    btn2 = InlineKeyboardButton(text='"PRO"', callback_data='pro')
    btn3 = InlineKeyboardButton(text='"FULL"', callback_data='full')
    kb.add(btn1, btn2, btn3)
    return kb

price1_courses_kb = InlineKeyboardMarkup()
kb2 = InlineKeyboardMarkup()
btn1 = InlineKeyboardButton(text='Курс «Python с нуля»', callback_data='course1')
btn2 = InlineKeyboardButton(text='Курс «Разработка Telegram-ботов»', callback_data='course2')
price1_courses_kb.add(btn1).add(btn2)

photo_lite = 'https://t.me/forbot_nikita/9'
photo_pro = 'https://t.me/forbot_nikita/10'
photo_full = 'https://t.me/forbot_nikita/8'
photo_course1 = 'https://t.me/forbot_nikita/11'
photo_course2 = 'https://t.me/forbot_nikita/12'

@dp.callback_query_handler(text=['lite', 'pro', 'full'])
async def first_btn_process(call: types.CallbackQuery):
    if call.data == 'lite':
        await call.answer(text='Благодарим за выбор тарифа "LITE"',
                          show_alert=True)
        await call.message.answer_photo(caption=text_lite,
                                        photo=photo_lite,
                                        parse_mode=ParseMode.MARKDOWN,
                                        reply_markup=pay_kb)
    elif call.data == 'pro':
        await call.answer(text='Благодарим за выбор тарифа "PRO"',
                          show_alert=True)
        await call.message.answer_photo(caption=text_pro,
                                        photo=photo_pro,
                                        parse_mode=ParseMode.MARKDOWN,
                                        reply_markup=pay_kb1)
    else:
        await call.answer(text='Благодарим за выбор тарифа "FULL"',
                          show_alert=True)
        await call.message.answer_photo(caption=text_full,
                                        photo=photo_full,
                                        parse_mode=ParseMode.MARKDOWN,
                                        reply_markup=pay_kb2)

@dp.callback_query_handler(text=['course1', 'course2'])
async def first_btn_process(call: types.CallbackQuery):
    if call.data == 'course1':
        await call.message.answer_photo(caption=text_course1,
                                        parse_mode=ParseMode.MARKDOWN,
                                        photo=photo_course1,
                                        reply_markup=pay_kb3)
    else:
        await call.message.answer_photo(caption=text_course2,
                                        parse_mode=ParseMode.MARKDOWN,
                                        photo=photo_course2,
                                        reply_markup=pay_kb4)

pay_kb = InlineKeyboardMarkup()
kb3 = InlineKeyboardMarkup()
btn1 = InlineKeyboardButton(text='Перейти к оплате', callback_data='pay')
btn2 = InlineKeyboardButton(text='Чат с менеджером', callback_data='mana', url='http://t.me/manager_fullstart')
pay_kb.add(btn1).add(btn2)

pay_kb1 = InlineKeyboardMarkup()
kb4 = InlineKeyboardMarkup()
btn1 = InlineKeyboardButton(text='Перейти к оплате', callback_data='pay1')
btn2 = InlineKeyboardButton(text='Чат с менеджером', callback_data='mana1', url='http://t.me/manager_fullstart')
pay_kb1.add(btn1).add(btn2)

pay_kb2 = InlineKeyboardMarkup()
kb5 = InlineKeyboardMarkup()
btn1 = InlineKeyboardButton(text='Перейти к оплате', callback_data='pay2')
btn2 = InlineKeyboardButton(text='Чат с менеджером', callback_data='mana2', url='http://t.me/manager_fullstart')
pay_kb2.add(btn1).add(btn2)

pay_kb3 = InlineKeyboardMarkup()
kb6 = InlineKeyboardMarkup()
btn1 = InlineKeyboardButton(text='Перейти к оплате', callback_data='pay3')
btn2 = InlineKeyboardButton(text='Чат с менеджером', callback_data='mana3', url='http://t.me/manager_fullstart')
pay_kb3.add(btn1).add(btn2)

pay_kb4 = InlineKeyboardMarkup()
kb7 = InlineKeyboardMarkup()
btn1 = InlineKeyboardButton(text='Перейти к оплате', callback_data='pay4')
btn2 = InlineKeyboardButton(text='Чат с менеджером', callback_data='mana4', url='http://t.me/manager_fullstart')
pay_kb4.add(btn1).add(btn2)




@dp.callback_query_handler(text=['pay', 'pay1', 'pay2'])
async def first_btn_process(call: types.CallbackQuery):
    if call.data == 'pay':
        await call.message.answer(text=text_pay,
                                  parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=manager_kb())
    elif call.data == 'pay1':
        await call.message.answer(text=text_pay1,
                                  parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=manager_kb())
    else:
        await call.message.answer(text=text_pay2,
                                  parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=manager_kb())


@dp.callback_query_handler(text=['pay3', 'pay4'])
async def first_btn_process(call: types.CallbackQuery):
    if call.data == 'pay3':
        await call.message.answer(text="У Вас имеется промокод на скидку?",
                                  reply_markup=pay_kb_course1())
    else:
        await call.message.answer(text="У Вас имеется промокод на скидку?",
                                  reply_markup=pay_kb_course2())

def pay_kb_course1():
    kb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text='Да', callback_data='yes')
    btn2 = InlineKeyboardButton(text='Нет', callback_data='no')
    kb.add(btn1, btn2)
    return kb

def pay_kb_course2():
    kb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text='Да', callback_data='yes1')
    btn2 = InlineKeyboardButton(text='Нет', callback_data='no1')
    kb.add(btn1, btn2)
    return kb

def pay_kb_course3():
    kb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text='Перейти к оплате', callback_data='yes3')
    kb.add(btn1)
    return kb

def pay_kb_course4():
    kb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text='Перейти к оплате', callback_data='yes4')
    kb.add(btn1)
    return kb

@dp.callback_query_handler(text=['yes', 'no'])
async def first_btn_process(call: types.CallbackQuery):
    if call.data == 'yes':
        await call.answer(text='Отправьте текстовое сообщение с промокодом',
                          show_alert=True)
        await call.message.answer(text='Введите промокод:')
    else:
        await call.message.answer(text=text_pay_course,
                                  parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=manager_kb())

@dp.callback_query_handler(text=['yes1', 'no1'])
async def first_btn_process(call: types.CallbackQuery):
    if call.data == 'yes1':
        await call.answer(text='Отправьте текстовое сообщение с промокодом',
                          show_alert=True)
        await call.message.answer(text='Введите промокод:')
    else:
        await call.message.answer(text=text_pay_course1,
                                  parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=manager_kb())

@dp.message_handler(text = 'SFPYTHON')
async def promo(message: types.Message):
    if message.text == 'SFPYTHON':
        await message.answer('Вам доступна *скидка 5%*, активируем?',
                             parse_mode=ParseMode.MARKDOWN,
                             reply_markup=pay_kb_course3())
    else:
        await message.answer('*Промокод неверный*, попробуем ещё раз?',
                             parse_mode=ParseMode.MARKDOWN,
                             reply_markup=pay_kb_course1())

@dp.message_handler(text = 'SFTGBOT')
async def promo(message: types.Message):
    if message.text == 'SFTGBOT':
        await message.answer('Вам доступна *скидка 10%*, активируем?',
                             parse_mode=ParseMode.MARKDOWN,
                             reply_markup=pay_kb_course4())
    else:
        await message.answer('*Промокод неверный*, попробуем ещё раз?',
                             parse_mode=ParseMode.MARKDOWN,
                             reply_markup=pay_kb_course2())

@dp.callback_query_handler(text=['yes3'])
async def first_btn_process(call: types.CallbackQuery):
    await call.message.answer(text=text_pay_course_promo,
                              parse_mode=ParseMode.MARKDOWN,
                              reply_markup=manager_kb())

@dp.callback_query_handler(text=['yes4'])
async def first_btn_process(call: types.CallbackQuery):
    await call.message.answer(text=text_pay_course1_promo,
                              parse_mode=ParseMode.MARKDOWN,
                              reply_markup=manager_kb())

text_logo = """
*Full Start - это высококлассное community профессионалов, специализирующихся на разработке многофункциональных 
Telegram-ботов для любого вида бизнеса и других сфер!* 
Telegram-бот станет удобным инструментом для привлечения внимания аудитории к Вашему проекту, он сможет собрать 
в любое время заявки и их обработать, поможет автоматизировать бизнес-процессы и рутинные действия человека. 

_С начала 2023 года наша команда реализовала 40+ Telegram-ботов разной сложности, практикуя фриланс_. 

В нашей команде имеются сертифицированные сотрудники, которые прошли курсы по направлению 
«Разработка Telegram-ботов на Python» в инновационном Университете Иннополис.
"""

text_price = """ Наша команда занимается разработкой чат-ботов в Telegram, но для того, что бы 
заинтересовать общество программированием, мы предоставляем образовательные курсы.\n
_Пожалуйста, выберите категорию услуги:_"""

text_contacts = """
Номер телефона: _8 (995) 294-55-32_
E-mail: _project@full-start.ru_
Адрес офиса: г. Нижний Новгород, ул. Московское шоссе, д. 12, 4 этаж, коворкинг «The Rooms»

*Работаем ежедневно с 10:00 до 22:00, в случае задержки ответа, напишите нашему менеджеру👍*
"""

text_sales = """
*Акции и скидки действующие на сегодняшний день*

Скидки:
_Скидка 5%_ действует на Разработку Telegram-бота по тарифам PRO и FULL

Промокоды:
*SFPYTHON* - промокод на _скидку 5%_ на курс «Python с нуля»
*SFTGBOT* - промокод на _скидку 10%_ на курс «Разработка Telegram-бота на Python»
"""

text_lite = """
*Тариф LITE*
Мы предлагаем качественную разработку Telegram-бота по тарифу LITE, который сможет привлечь внимание потенциальных клиентов, рассказать про Вашу деятельность. 

Разработка чат-бота по данному тарифу не включает в себя внедрение сложных интеграций и многофункционального взаимодействия с пользователями. 

По данному тарифу предполагается создание бота-информатора (Например: Чат-бот визитка, Wikipedia-бот, Бот-всезнайка). 

*Сроки: от 2 до 4 дней.*

_Наша команда оказывает поддержку после сдачи проекта._
"""

text_pro = """
*Тариф PRO*
Наша команда предлагает разработку Telegram-бота по тарифу PRO для Вашего бизнеса и любых других потребностей, 
многофункциональный бот будет разработан согласно всем Вашим требованиям, которые мы обсудим во время личной 
или онлайн-встречи. 

Представленный тариф предполагает возможность реализации небольшого интернет-магазина(т.е. принятия платежей), бота для общения с клиентами, бота-конвертера(обменник валюты), бота-психолога и многое другое. 

*Сроки: от 5 до 8 дней.*

_Наша команда оказывает поддержку после сдачи проекта._
"""

text_full = """
*Тариф FULL*
Наша команда предлагает разработку эксклюзивного и индивидуального Telegram-бота по тарифу FULL, написанного с помощью языка 
программирования Python, безграничного в своём функционале! 

_Представленный тариф не имеет лимита различных интеграций и все детали обсуждаются исключительно в индивидуальном порядке. 
Во время работы над проектом мы поможем Вам выбрать наиболее удобный для пользователей функционал, который будет приносить им удовольствие от использования Вашего бота._ 

*Срок реализации проекта: до 14 дней.*

_Наша команда оказывает особую поддержку после сдачи проекта по тарифу FULL._
"""

text_course1 = """
_Курс «Python с нуля» поможет начать программировать на Python человеку, который никогда даже не углублялся в эту сферу!_

*Длительность курса 3 месяца.*

_В программу закладывается занятий на 3,2 часа в неделю._
_Всего 38,4 часа программирования за 3 месяца, без учёта домашних заданий._

*Преимущество этого курса в том, что все занятия проводятся индивидуально.*

Эксклюзивным подходом к обучению в данной программе является работа над мини-проектами каждую неделю по пройденной теме.
(Применение теории на практике, с подробным разбором для детального понимания кода) 

Оплата курса возможна как сразу полностью, так и ежемесячно.
"""

text_course2 = """
_Курс «Разработка Telegram-ботов на Python» предусматривает узкоспециализированную программу обучения по разработке 
чат-ботов в Телеграмм, с помощью фреймворка aiogram._

*Длительность курса 3 месяца.*
_В программу закладывается 3 часа занятий в неделю._
_Всего 36 часов программирования за 3 месяца, без учёта домашних заданий._

*Преимущество этого курса в том, что все занятия проводятся индивидуально.*

Каждые две недели предусмотрена работа над созданием чат-ботов по пройденным темам, а в конце курса - разработка полноценного проекта. 

Оплата курса возможна как сразу полностью, так и ежемесячно. 
"""

text_pay = """
*Тариф "LITE"*

Стоимость: от 3000₽
Скидка: 0₽
*Итого к оплате: от 3000₽*

*Данные для оплаты*
Номер карты: 2200 7006 0120 2509
Получатель: Сюхин Никита Александрович 
Банк-получатель: АО «Тинькофф Банк»

_После оплаты просим Вас отправить скриншот менеджеру_
"""

text_pay1 = """
*Тариф "PRO"*
*Для Вас активирована скидка 5% на выбранную услугу*

Стоимость: от 5.000₽
Скидка: от 250₽
*Итого к оплате: от 4.500₽*

*Данные для оплаты*
Номер карты: 2200 7006 0120 2509
Получатель: Сюхин Никита Александрович 
Банк-получатель: АО «Тинькофф Банк»

_После оплаты просим Вас отправить скриншот менеджеру_
"""
text_pay2 = """
*Тариф "FULL"*
*Для Вас активирована скидка 5% на выбранную услугу*

Стоимость: от 10.000₽
Скидка: от 500₽
*Итого к оплате: от 9.500₽*

*Данные для оплаты*
Номер карты: 2200 7006 0120 2509
Получатель: Сюхин Никита Александрович 
Банк-получатель: АО «Тинькофф Банк»

_После оплаты просим Вас отправить скриншот менеджеру_
"""

text_pay_course = """
*Курс «Python с нуля»*

Стоимость: 19.200₽
Скидка: 0₽
*Итого к оплате: 19.200₽*

*Данные для оплаты*
Номер карты: 2200 7006 0120 2509
Получатель: Сюхин Никита Александрович 
Банк-получатель: АО «Тинькофф Банк»

_После оплаты просим Вас отправить скриншот менеджеру_
"""

text_pay_course1 = """
*Курс «Разработка Telegram-ботов»*

Стоимость: 15.000₽
Скидка: 0₽
*Итого к оплате: 15.000₽*

*Данные для оплаты*
Номер карты: 2200 7006 0120 2509
Получатель: Сюхин Никита Александрович 
Банк-получатель: АО «Тинькофф Банк»

_После оплаты просим Вас отправить скриншот менеджеру_
"""

text_pay_course_promo = """
*Курс «Python с нуля»*

Стоимость: 19.200₽
Скидка: 960₽
*Итого к оплате: 18.240₽*

*Данные для оплаты*
Номер карты: 2200 7006 0120 2509
Получатель: Сюхин Никита Александрович 
Банк-получатель: АО «Тинькофф Банк»

_После оплаты просим Вас отправить скриншот менеджеру_
"""

text_pay_course1_promo = """
*Курс «Разработка Telegram-ботов»*

Стоимость: 15.000₽
Скидка: 1.500₽
*Итого к оплате: 13.500₽*

*Данные для оплаты*
Номер карты: 2200 7006 0120 2509
Получатель: Сюхин Никита Александрович 
Банк-получатель: АО «Тинькофф Банк»

_После оплаты просим Вас отправить скриншот менеджеру_
"""

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
