import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties

# ========== CONFIG ==========
BOT_TOKEN = "8418509184:AAE4XOYgXovlMA3LZRZQkuJ6qZ1rBjbHFGE"
ADMIN_CHAT_ID = 123456789
INVITE_CODE = "65880168"
CONTRACT = "TRXwTm65dF8QotHwdcQJGzp8KVFhAiAiAi"
# ============================

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
r = Router()
dp.include_router(r)

user_lang = {}
DEFAULT_LANG = "en"

# ============================================================
#                 MULTILANGUAGE TEXT (PREMIUM)
# ============================================================
T = {
"welcome":{
"en":"<b>Welcome to AI TRON Premium Assistant.</b>\nYour step-by-step joining guide is ready below.",
"zh":"<b>欢迎来到 AI TRON 高级助手。</b>\n您的加入步骤指引如下。",
"ru":"<b>Добро пожаловать в AI TRON Premium Assistant.</b>\nВаше руководство готово ниже.",
"hi":"<b>AI TRON प्रीमियम सहायता में आपका स्वागत है।</b>\nनीचे पूरा गाइड उपलब्ध है।",
"ph":"<b>Welcome sa AI TRON Premium Assistant.</b>\nNarito ang full joining guide mo."
},

"start_join":{
"en":"To join AI TRON, you must complete 3 required steps:\n\n"
     "1️⃣ Binding (2 TRX → get 1 TRX back)\n"
     "2️⃣ Open account (2000 TRX or 400 TRX)\n"
     "3️⃣ Add liquidity after 24 hours\n\n"
     "I’ll guide you through each part below.",
},

"wallet":{
"en":"Do you already have a TRON wallet (TP Wallet or TronLink)?",
},

"wallet_help":{
"en":"Please install:\n• TP Wallet\n• TronLink\n\nAfter installing, return to /start."
},

"bind":{
"en":f"<b>Step 1 — Binding</b>\n\n"
     f"Send exactly <b>2 TRX</b> to:\n<code>{CONTRACT}</code>\n\n"
     f"Enter inviter code:\n<code>{INVITE_CODE}</code>\n\n"
     f"🔥 You MUST receive <b>1 TRX</b> back. If not, binding failed.",
},

"plan_intro":{
"en":"Choose your starting plan below:",
},

"planA":{
"en":f"<b>Plan A — 2000 TRX</b>\n\n"
     f"Send:\n<code>2000 TRX</code>\nTo:\n<code>{CONTRACT}</code>\n\n"
     f"You will receive:\n• Personal invite code\n• 6000 TRX airdrop credit",
},

"planB":{
"en":f"<b>Plan B — 400 TRX</b>\n\n"
     f"Send:\n<code>400 TRX</code>\nTo:\n<code>{CONTRACT}</code>\n\n"
     f"You will receive:\n• Personal invite code\n• 1200 TRX airdrop credit",
},

"liquidity":{
"en":f"<b>Step 3 — Adding Liquidity</b>\n\n"
     f"1) Send 3000 TRX (Plan A) or 600 TRX (Plan B)\n"
     f"2) After 24 hours → send 20 TRX or 6 TRX\n\n"
     f"Contract returns:\n• 80 TRX (A)\n• 16 TRX (B)\n\n"
     f"And mints the <b>AI Token</b>.",
},

"share":{
"en":f"<b>Rewards, Sharing & Levels</b>\n\n"
     f"Plan A: 30% direct push\nPlan B: 20% direct push\n\n"
     f"Generations: Up to 30 gens.\n"
     f"Performance query: Send 3 TRX to the contract.",
},

"safety":{
"en":"<b>Safety Notes</b>\n\n• 100% on-chain\n• No admin control\n• Funds never leave your wallet\n• Smart contract automated",
},

"contract":{
"en":f"<b>Contract Address:</b>\n<code>{CONTRACT}</code>"
},

"faq":{
"en":"Select a FAQ topic below:",
},

"sent":{
"en":"✅ Sent to admin."
}
}

def t(key, lang="en"):
    return T[key].get(lang, T[key]["en"])

# ============================================================
#                    BUTTONS (PREMIUM)
# ============================================================
def kb_home():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✨ Start Joining", callback_data="join")],
        [InlineKeyboardButton(text="💧 Add Liquidity", callback_data="liq")],
        [InlineKeyboardButton(text="📈 Rewards / Sharing", callback_data="share")],
        [InlineKeyboardButton(text="📜 Contract", callback_data="contract")],
        [InlineKeyboardButton(text="❓ FAQ", callback_data="faq")],
        [InlineKeyboardButton(text="👤 Contact Support", url="https://t.me/AiTronSupport")]
    ])

def kb_back():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅ Back", callback_data="home")]
    ])

def kb_yes_no():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Yes", callback_data="yes"),
         InlineKeyboardButton(text="No", callback_data="no")]
    ])

def kb_plans():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 Plan A — 2000 TRX", callback_data="A")],
        [InlineKeyboardButton(text="⭐ Plan B — 400 TRX", callback_data="B")],
        [InlineKeyboardButton(text="⬅ Back", callback_data="home")]
    ])

def kb_faq():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📌 How to Join?", url="https://medium.com/@troinai_ardp/how-to-join-ai-tron-binding-account-opening-and-liquidity-participation-explained-f9b3f154721e")],
        [InlineKeyboardButton(text="⛓ Binding Failed", url="https://medium.com/@troinai_ardp/binding-failed-no-trx-returned-troubleshooting-guide-1d06d5b01a33")],
        [InlineKeyboardButton(text="💸 TRX Not Returning?", url="https://medium.com/@troinai_ardp/binding-failed-no-trx-returned-troubleshooting-guide-1d06d5b01a33")],
        [InlineKeyboardButton(text="💎 Plan A vs B", url="https://medium.com/@troinai_ardp/plan-a-vs-plan-b-whats-the-difference-435479cbede2")],
        [InlineKeyboardButton(text="⬅ Back", callback_data="home")]
    ])


# ============================================================
#                      HANDLERS
# ============================================================
@r.message(CommandStart())
async def start(m: Message):
    await m.answer(t("welcome"), reply_markup=kb_home())

@r.callback_query(F.data == "home")
async def home(cb: CallbackQuery):
    await cb.message.edit_text(t("welcome"), reply_markup=kb_home())

@r.callback_query(F.data == "join")
async def join_start(cb: CallbackQuery):
    await cb.message.edit_text(t("start_join"), reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➡ Continue", callback_data="wallet")],
            [InlineKeyboardButton(text="⬅ Back", callback_data="home")]
        ]
    ))

@r.callback_query(F.data == "wallet")
async def ask_wallet(cb: CallbackQuery):
    await cb.message.edit_text(t("wallet"), reply_markup=kb_yes_no())

@r.callback_query(F.data == "no")
async def no_wallet(cb: CallbackQuery):
    await cb.message.edit_text(t("wallet_help"), reply_markup=kb_back())

@r.callback_query(F.data == "yes")
async def wallet_yes(cb: CallbackQuery):
    await cb.message.edit_text(t("bind"), reply_markup=kb_plans())

@r.callback_query(F.data == "A")
async def choose_A(cb: CallbackQuery):
    await cb.message.edit_text(t("planA"), reply_markup=kb_back())

@r.callback_query(F.data == "B")
async def choose_B(cb: CallbackQuery):
    await cb.message.edit_text(t("planB"), reply_markup=kb_back())

@r.callback_query(F.data == "liq")
async def liq(cb: CallbackQuery):
    await cb.message.edit_text(t("liquidity"), reply_markup=kb_back())

@r.callback_query(F.data == "share")
async def share(cb: CallbackQuery):
    await cb.message.edit_text(t("share"), reply_markup=kb_back())

@r.callback_query(F.data == "contract")
async def contract(cb: CallbackQuery):
    await cb.message.edit_text(t("contract"), reply_markup=kb_back())

@r.callback_query(F.data == "safety")
async def safety(cb: CallbackQuery):
    await cb.message.edit_text(t("safety"), reply_markup=kb_back())

@r.callback_query(F.data == "faq")
async def faq(cb: CallbackQuery):
    await cb.message.edit_text(t("faq"), reply_markup=kb_faq())

FAQ_ANS = {
"faq_join":"To join: Bind → Open Account (2000/400) → Liquidity → Daily rewards.",
"faq_bind":"Binding fails if invite code missing, wrong TRX amount, or network delay.",
"faq_return":"TRX return delay is normal during TRON congestion.",
"faq_diff":"Plan A = higher capital, higher rewards. Plan B = lower capital, smaller rewards."
}

@r.callback_query(F.data.startswith("faq_"))
async def faq_answer(cb: CallbackQuery):
    data = cb.data
    await cb.message.edit_text(FAQ_ANS[data], reply_markup=kb_faq())

@r.callback_query(F.data == "support")
async def support(cb: CallbackQuery):
    await cb.message.answer("Please type your question.")

@r.message()
async def forward(m: Message):
    if m.chat.id != ADMIN_CHAT_ID:
        await bot.send_message(ADMIN_CHAT_ID, f"Message from {m.from_user.id}:\n{m.text}")
        await m.answer("Message sent to admin.")
    else:
        await m.answer("OK.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
