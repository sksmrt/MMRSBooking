from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class AdminStates(StatesGroup):
    awaiting_rejection_comment = State()

@router.callback_query(F.data.startswith("admin_confirm:"))
async def admin_accept(call: types.CallbackQuery):
    user_id = int(call.data.split(":")[1])
    await call.bot.send_message(user_id, "✅ Ваша бронь подтверждена!")
    await call.message.edit_reply_markup()
    await call.answer("Подтверждено")


@router.callback_query(F.data.startswith("admin_reject:"))
async def admin_reject(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.split(":")[1]
    await call.message.answer("🖋 Введите комментарий к отказу:")
    await state.set_state(AdminStates.awaiting_rejection_comment)
    await state.update_data(reject_user=user_id)
    await call.answer()

@router.message(AdminStates.awaiting_rejection_comment)
async def send_rejection_comment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.bot.send_message(data['reject_user'], f"❌ Ваша бронь отклонена. Причина: {message.text}")
    await message.answer("Отказ отправлен пользователю.")
    await state.clear()
