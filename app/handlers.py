from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

router = Router()


class Reg(StatesGroup):
    name = State()
    number = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.reply(f"Hi!\nYour's ID: {message.from_user.id}\nYour's name: {message.from_user.first_name}",
                        reply_markup=kb.main)


@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer("Выберите категорию товара", reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer("Вы выбрали категорию")
    await callback.message.answer('Выберите товар',
                                  reply_markup=await kb.items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def category(callback: CallbackQuery):
    item_data = await rq.get_item(callback.data.split('_')[1])
    await callback.answer("Вы выбрали товар")
    await callback.message.answer(f'название: {item_data.name}\nОписание: {item_data.description}\nЦена: {item_data.price}')





@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("help")


@router.message(F.text  == 'What?')
async def cmd_what(message: Message):
    await message.answer("That")


@router.message(F.photo)
async def cmd_what(message: Message):
    await message.answer(f"ID фото: {message.photo[-1].file_id}")


@router.message(Command("get_photo"))
async def cmd_help(message: Message):
    await message.answer_photo(photo="AgACAgIAAxkBAAMeaJhjgv1JyQfD7I1-3R0u5BoP7LAAAsnzMRsxmcFIqSqr7g5FLh8BAAMCAANtAAM2BA",
                               caption="Picture")

@router.callback_query(F.data == "smth1")
async def cmd_smth1(callback: CallbackQuery):
    await callback.answer('Your choice: Smth1', show_alert=True)
    await callback.message.edit_text("hi!", reply_markup=await kb.inline_cars())
    # await callback.message.answer("hi!")


@router.message(Command('reg'))
async def reg_one(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer("Enter your name")

@router.message(Reg.name)
async def reg_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.number)
    await message.answer("Enter your number")

@router.message(Reg.number)
async def reg_three(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    await message.answer(f"Thanks\nName: {data['name']}\nNumber{data['number']}")
    await state.clear()