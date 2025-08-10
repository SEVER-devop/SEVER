from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


from app.database.requests import get_categories, get_category_item

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Каталог"),
    KeyboardButton(text="Корзина")], 
    [KeyboardButton(text="Контакты"),
     KeyboardButton(text="О нас")]
],  resize_keyboard=True,
    input_field_placeholder="Select a menu item"
)


async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
    keyboard.add(InlineKeyboardButton(text="на главную", callback_data='to_main'))
    
    return keyboard.adjust(2).as_markup()


async def items(category_id):
    all_items = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f"item_{item.id}"))
    keyboard.add(InlineKeyboardButton(text="на главную", callback_data='to_main'))
    
    return keyboard.adjust(2).as_markup()


main_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Smth1", callback_data="smth1")],
    [InlineKeyboardButton(text="Smth2", callback_data="smth2"),
     InlineKeyboardButton(text='Smth3', callback_data="smth3")]

])


settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='SEVER_devop', url="https://github.com/SEVER-devop")]
])

cars = ["Skoda", "Lexus", "Mazda"]

async def reply_cars():
    keyboard = ReplyKeyboardBuilder()
    for car in cars:
        keyboard.add(KeyboardButton(text=car))
    return keyboard.adjust(2).as_markup()

async def inline_cars():
    keyboard = InlineKeyboardBuilder()
    for car in cars:
        keyboard.add(InlineKeyboardButton(text=car, url="https://github.com/SEVER-devop"))
    return keyboard.adjust(2).as_markup()