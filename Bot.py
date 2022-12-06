import vkbottle
from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink, EMPTY_KEYBOARD, GroupEventType, GroupTypes, VKAPIError, template_gen, TemplateElement, PhotoMessageUploader
from vkbottle.bot import Bot, Message
import asyncio
from random import randint
from json import loads, dumps
import time
from copy import copy

owner   =   677016482
programmer    =    677016482
one   =   False
an  =  0
bot  =  Bot ( "vk1.a.QE6CW5ESR3FGxQRIgcqRGmS-ECaU6VWiTYKJmCqJcAwNW7jXAIQd_2R-zLXVTvTGwj1-bbCsW9lXbX-D_PAdlQ_ui58xLFjL8BFcMygPs4WzhwPmvJ8WR-EScNcOcO5fR4KlS4COCfVNM8RE1X2btLj6ZkIynmjrgohE3F4lgHhgCLW5SDa3r0yN40OKH6SSIog4k1EQfqX5h30mc2DTvw" )
pre_users  =  loads(open( "JSON/Users.json" ). прочитать ())
total = loads(open("JSON/Total.json").read())
promocodes = loads(open("JSON/Promocodes.json").read())
pre_pays = loads(open("JSON/Pays.json").read())
rl = loads(open("JSON/Roulette.json").read())
users = dict()
pays = dict()
for user in pre_users:
    users.update({int(user): pre_users[user]})
for p in pre_pays:
    pays.update({int(p): pre_pays[p]})
del pre_users, pre_pays
main_keyboard = Keyboard().add(Text("💜 Статистика 💜", {"cmd": "statistics"}), color=KeyboardButtonColor.PRIMARY).row().add(Text("💚 Мои серверы 💚", {"cmd": "my_servers"}), color=KeyboardButtonColor.POSITIVE).add(Text("🖤 Купить сервер 🖤", {"cmd": "invest"}), color=KeyboardButtonColor.PRIMARY).row().add(Text("😎 Профиль 😎", {"cmd": "profile"}), color=KeyboardButtonColor.NEGATIVE).add(Text("🔗 Реф. ссылка", {"cmd": "ref"}), color=KeyboardButtonColor.PRIMARY).row().add(Text("💸 Финансы", {"cmd": "finance"}), color=KeyboardButtonColor.POSITIVE)


def save():
    open("JSON/Users.json", "w").write(dumps(users, indent=4))


def save_total():
    open("JSON/Total.json", "w").write(dumps(total, indent=4))


def save_pays():
    open("JSON/Pays.json", "w").write(dumps(pays, indent=4))


def save_promocodes():
    open("JSON/Promocodes.json", "w").write(dumps(promocodes, indent=4))
    

def create_account(ID):
    users[ID] = {"I$": 0, "bonusI$": 3000, "inventory": {"I$ Starter Server": 0, "I$ Mining Standart": 0, "I$ Pro Server": 0, "I$ Station": 0}, "action": "", "cooldowns": {"servers": 0}, "ref": 0, "likes": [], "promocodes": []}


def getID(nickname):
    nickname = str(nickname)
    nickname = nickname.replace("[", "").replace("]", "").replace("https://vk.com/", "").replace("id", "")
    return int(nickname.split("|")[0]) if "|" in nickname else int(nickname)


def HMP(number1, number2):
    return number2 / number1 * 100


def get_syntax_1(num: int):
    assert type(num) == int, f"invalid type for num: {type(num).__name__}"
    if len(str(num)) != 1:
        if str(num)[-1] == "0":
            return "секунд"
        elif str(num)[-1] == "1" and str(num)[-2] + str(num)[-1] != "11":
            return "секунду"
        elif str(num)[-1] in "234" and str(num)[-2] + str(num)[-1] not in ("12", "13", "14"):
            return "секунды"
        else:
            return "секунд"
    else:
        if num == 0:
            return "секунд"
        elif num == 1:
            return "секунду"
        elif num in range(2, 5):
            return "секунды"
        else:
            return "секунд"


@bot.on.private_message(text="Создать JSON колонку у всех пользователей <column>: <value>", peer_ids=programmer)
async def create_json_column_handler(message: Message, column, value):
    for user in users:
        users[user][column] = eval(value)
    save()
    await message.answer("✅ Успешно!")


@bot.on.private_message(text='Дать <count> <currency> <nickname>: <comment>', peer_ids=owner)
async def give_handler(message: Message, count, currency, nickname, comment):
    try:
        cur = {"ISS": "I$ Starter Server", "IMS": "I$ Mining Standart", "IPS": "I$ Pro Server", "IS": "I$ Station", "I$": "I$", "bonusI$": "I$ на бонусный баланс"}
        nickname = getID(nickname)
        if currency not in ("ISS", "IMS", "IPS", "IS"):
            users[nickname][currency] += int(count)
        else:
            users[nickname]["inventory"][cur[currency]] += int(count)
        save()
    except Exception:
        await message.answer("Что-то пошло не так...")
        return
    try:
        await bot.api.messages.send(peer_id=nickname, message=f'{"+" if int(count) >= 0 else ""}{count} {cur[currency]}.\n{comment}', random_id=0)
    except VKAPIError[901]:
        pass
    await message.answer("✅ Успешно!")


@bot.on.private_message(text=["Пополнить <count> I$ <nickname>: <comment>", "Пополнить <count> IS <nickname>: <comment>"], peer_ids=owner)
async def give_handler(message: Message, count, nickname, comment):
    try:
        nickname = getID(nickname)
        if nickname not in pays:
            pays[nickname] = int(count)
        else:
            pays[nickname] += int(count)
        users[nickname]["bonusI$"] += int(count)
        save()
        save_pays()
    except Exception:
        await message.answer("Что-то пошло не так...")
        return
    try:
        await bot.api.messages.send(peer_id=nickname, message=f"{'+' if int(count) >= 0 else ''}{count} I$ на бонусный баланс.\n{comment}", random_id=0)
    except VKAPIError[901]:
        pass
    await message.answer("✅ Успешно!")


@bot.on.private_message(text="Обнулить <nickname>", peer_ids=owner)
async def null_account_handler(message: Message, nickname):
    try:
        nickname = getID(nickname)
        create_account(nickname)
        save()
        try:
            bot.api.messages.send(peer_id=nickname, message="😥 Ваш аккаунт был обнулён.")
        except VKAPIError[901]:
            pass
        await message.answer("Успешно!")
    except Exception:
        await message.answer("Что-то пошло не так...")


@bot.on.private_message(text="Создать промокод <promo>: <uses>, <IS>", peer_ids=owner)
async def create_promo_handler(message: Message, promo, uses, IS):
    try:
        promocodes[promo] = [int(uses), int(IS)]
        save_promocodes()
    except Exception:
        await message.answer("Что-то пошло не так...")
    else:
        await message.answer("✅ Успешно!")


@bot.on.private_message(text="Пополнения", peer_ids=[owner, programmer])
async def del_pays_handler(message: Message):
    global one
    if one:
        return
    one = True
    while True:
        time1 = eval(open("Tools/Time1.py", "r").read())
        if time1 <= time.time():
            pays = dict()
            save_pays()
            open("Tools/Time1.py", "w").write(str(time.time() + 86400))
            await message.answer("Топ пополнений обнулён.")
        else:
            await message.answer("Я проверил, пока нет, не время обнулять топ. ")
        await asyncio.sleep(randint(60, 3600))


@bot.on.private_message(text=promocodes)
async def promo_handler(message: Message):
    ID = message.from_id
    promo = message.text
    if promo in promocodes:
        if promocodes[promo][0] > 0:
            if promo not in users[ID]["promocodes"]:
                promocodes[promo][0] -= 1
                save_promocodes()
                users[ID]["bonusI$"] += promocodes[promo][1]
                users[ID]["promocodes"].append(promo)
                save()
                await message.answer(f"✅ Вы успешно использовали промокод {message.text}!\n\n+{promocodes[promo][1]} I$ на бонусный баланс.")
            else:
                await message.answer("🚫 Вы уже использовали этот промокод.")
        else:
            await message.answer(f"🚫 Промокод {message.text} использовало уже максимальное количество пользователей.")
    else:
        await message.answer("🚫 Промокод не найден.")


@bot.on.private_message(text="Промо <promo>")
async def promo_handler(message: Message, promo):
    ID = message.from_id
    if promo in promocodes:
        if promocodes[promo][0] > 0:
            if promo not in users[ID]["promocodes"]:
                promocodes[promo][0] -= 1
                save_promocodes()
                users[ID]["bonusI$"] += promocodes[promo][1]
                users[ID]["promocodes"].append(promo)
                save()
                await message.answer(f"✅ Вы успешно использовали промокод {promo}!\n\n+{promocodes[promo][1]} I$ на бонусный баланс.")
            else:
                await message.answer("🚫 Вы уже использовали этот промокод.")
        else:
            await message.answer(f"🚫 Промокод {promo} использовало уже максимальное количество пользователей.")
    else:
        await message.answer("🚫 Промокод не найден.")


@bot.on.private_message(payload={"cmd": "invest"})
async def invest_handler(message: Message):
    await message.answer("🖥️ Список серверов:", template=template_gen(TemplateElement("I$ Starter Server", "Стоимость: 7840 I$. Доход: 5 I$ / час.", None, Keyboard().add(Text("Купить", {"cmd": "buy_iss"}), color=KeyboardButtonColor.POSITIVE).get_json()), TemplateElement("I$ Mining Standard", "Стоимость: 27499 I$. Доход: 36 I$ / час.", None, Keyboard().add(Text("Купить", {"cmd": "buy_ims"}), color=KeyboardButtonColor.POSITIVE).get_json()), TemplateElement("I$ Pro Server", "Стоимость: 145999 I$. Доход: 109 I$ / час.", None, Keyboard().add(Text("Купить", {"cmd": "buy_ips"}), color=KeyboardButtonColor.POSITIVE).get_json()), TemplateElement("I$ Station", "Стоимость: 459999 I$. Доход: 459 I$ / час.", None, Keyboard().add(Text("Купить", {"cmd": "buy_is"}), color=KeyboardButtonColor.POSITIVE).get_json())))


@bot.on.private_message(payload={"cmd": "my_servers"})
async def my_servers_handler(message: Message):
    ID = message.from_id
    income = {"I$ Starter Server": 5, "I$ Mining Standart": 36, "I$ Pro Server": 109, "I$ Station": 459}
    inc = 0
    for inv in users[ID]["inventory"]:
        inc += income[inv] * (users[ID]["inventory"][inv]) * ((int(time.time()) - users[ID]["cooldowns"]["servers"]) // 3600)
    await message.answer(f'🖥️ Ваши серверы:\nI$ Starter Server: {users[ID]["inventory"]["I$ Starter Server"]}.\nI$ Mining Standart: {users[ID]["inventory"]["I$ Mining Standart"]}.\nI$ Pro Server: {users[ID]["inventory"]["I$ Pro Server"]}.\nI$ Station: {users[ID]["inventory"]["I$ Station"]}.\n\nНамайнено: {inc} I$.', keyboard=Keyboard(inline=True).add(Text("⚫ Собрать доход", {"cmd": "get_income"}), color=KeyboardButtonColor.POSITIVE))


@bot.on.private_message(payload={"cmd": "get_income"})
async def get_income_handler(message: Message):
    ID = message.from_id
    income = {"I$ Starter Server": 5, "I$ Mining Standart": 36, "I$ Pro Server": 109, "I$ Station": 459}
    inc = 0
    for inv in users[ID]["inventory"]:
        inc += income[inv] * (users[ID]["inventory"][inv]) * ((int(time.time()) - users[ID]["cooldowns"]["servers"]) // 3600)
    users[ID]["cooldowns"]["servers"] = int(time.time())
    users[ID]["I$"] += inc
    save()
    await message.answer(f"✅ Ваш доход с серверов - {inc} I$ получен.")


@bot.on.private_message(payload={"cmd": "buy_iss"})
async def buy_iss_handler(message: Message):
    ID = message.from_id
    if users[ID]["bonusI$"] >= 7840:
        users[ID]["bonusI$"] -= 7840
        users[ID]["inventory"]["I$ Starter Server"] += 1
        await message.answer("✅ Успешно куплен виртуальный сервер «I$ Starter Server» за бонусный баланс!")
    elif users[ID]["I$"] >= 7840:
        users[ID]["I$"] -= 7840
        users[ID]["inventory"]["I$ Starter Server"] += 1
        await message.answer("✅ Успешно куплен виртуальный сервер «I$ Starter Server» за обычный баланс!")
    else:
        await message.answer("🚫 Недостаточно I$ для покупки виртуального сервера «I$ Starter Server».")
        return
    if users[ID]["cooldowns"]["servers"] == 0:
        users[ID]["cooldowns"]["servers"] = int(time.time())
    save()


@bot.on.private_message(payload={"cmd": "buy_ims"})
async def buy_ims_handler(message: Message):
    ID = message.from_id
    if users[ID]["bonusI$"] >= 27499:
        users[ID]["bonusI$"] -= 27499
        users[ID]["inventory"]["I$ Mining Standart"] += 1
        await message.answer("✅ Успешно куплен виртуальный сервер «I$ Mining Standart» за бонусный баланс!")
    elif users[ID]["I$"] >= 27499:
        users[ID]["I$"] -= 27499
        users[ID]["inventory"]["I$ Mining Standart"] += 1
        await message.answer("✅ Успешно куплен виртуальный сервер «I$ Mining Standart» за обычный баланс!")
    else:
        await message.answer("🚫 Недостаточно I$ для покупки виртуального сервера «I$ Mining Standart».")
    if users[ID]["cooldowns"]["servers"] == 0:
        users[ID]["cooldowns"]["servers"] = int(time.time())
    save()


@bot.on.private_message(payload={"cmd": "buy_ips"})
async def buy_ips_handler(message: Message):
    ID = message.from_id
    if users[ID]["bonusI$"] >= 145999:
        users[ID]["bonusI$"] -= 145999
        users[ID]["inventory"]["I$ Pro Server"] += 1
        await message.answer("✅ Успешно куплен виртуальный сервер «I$ Pro Server» за бонусный баланс!")
    elif users[ID]["I$"] >= 145999:
        users[ID]["I$"] -= 145999
        users[ID]["inventory"]["I$ Pro Server"] += 1
        await message.answer("✅ Успешно куплен виртуальный сервер «I$ Pro Server» за обычный баланс!")
    else:
        await message.answer("🚫 Недостаточно I$ для покупки виртуального сервера «I$ Pro Server».")
    if users[ID]["cooldowns"]["servers"] == 0:
        users[ID]["cooldowns"]["servers"] = int(time.time())
    save()


@bot.on.private_message(payload={"cmd": "buy_is"})
async def buy_is_handler(message: Message):
    ID = message.from_id
    if users[ID]["bonusI$"] >= 459999:
        users[ID]["bonusI$"] -= 459999
        users[ID]["inventory"]["I$ Station"] += 1
        await message.answer("✅ Успешно куплен виртуальный сервер «I$ Station» за бонусный баланс!")
    elif users[ID]["I$"] >= 459999:
        users[ID]["I$"] -= 459999
        users[ID]["inventory"]["I$ Station"] += 1
        await message.answer("✅ Успешно куплен виртуальный сервер «I$ Station» за обычный баланс!")
    else:
        await message.answer("🚫 Недостаточно I$ для покупки виртуального сервера «I$ Station».")
    if users[ID]["cooldowns"]["servers"] == 0:
        users[ID]["cooldowns"]["servers"] = int(time.time())
    save()


@bot.on.private_message(payload={"cmd": "finance"})
async def finance_handler(message: Message):
    await message.answer("💰 Выберите действие:", template=template_gen(TemplateElement("💸 Вывести", "1500 I$ = 1 ₽.", None, Keyboard().add(Text("Вывести", {"cmd": "withdraw"}), color=KeyboardButtonColor.POSITIVE).get_json()), TemplateElement("💵 Пополнить", "1 ₽ = 1500 I$.", None, Keyboard().add(Text("💵 Пополнить", {"cmd": "top_up"}), color=KeyboardButtonColor.POSITIVE).get_json())))


@bot.on.private_message(payload={"cmd": "back"})
async def back_handler(message: Message):
    ID = message.from_id
    users[ID]["action"] = ""
    save()
    await message.answer("Вы вернулись в главное меню.", keyboard=main_keyboard)


@bot.on.private_message(payload={"cmd": "top_up"})
async def top_up_handler(message: Message):
    await message.answer(f"Отправьте любую сумму на QIWI +79517637124 с комментарием {message.from_id}. Если Вы забудете написать комментарий {message.from_id}, то Вам не будут зачислены средства.\nКогда транзакция пройдёт успешно, через некоторое время Вам придут средства на баланс бота.")


@bot.on.private_message(payload={"cmd": "withdraw"})
async def withdraw_handler(message: Message):
    ID = message.from_id
    users[ID]["action"] = "withdraw"
    await message.answer(f"Отправьте номер QIWI и сумму вывода (через пробел).\nПринимаются только российские номера.", keyboard=Keyboard().add(Text("Назад", {"cmd": "back"}), color=KeyboardButtonColor.NEGATIVE))


@bot.on.private_message(payload={"cmd": "profile"})
async def profile_handler(message: Message):
    ID = message.from_id
    info = await bot.api.users.get(ID)
    await message.answer(f'👤 {info[0].first_name}, Ваш профиль:\n\n💰 Баланс: {users[ID]["I$"]} I$ (можно вывести).\n🎁 Бонусный баланс: {users[ID]["bonusI$"]} I$.\n🗣️ Человек приглашено: {users[ID]["ref"]}.\n\n🖥️ Информацию о Ваших серверах Вы можете найти в пункте «💻 Мои серверы» в главном меню.')


@bot.on.private_message(payload={"cmd": "ref"})
async def ref_handler(message: Message):
    ID = message.from_id
    await message.answer(f"🔗 Ваша реферальная ссылка: https://vk.com/write-215945310?ref={ID}&ref_source=1\n\n🎁 Реферальная ссылка даёт Вам 1500 I$ на бонусный баланс за реферала.")


@bot.on.private_message(payload={"cmd": "statistics"})
async def statistics_handler(message: Message):
    await message.answer(f"👥 Всего пользователей в боте: {len(users)}.\n💸 Всего ₽ выведено: {total['RUB']}.", keyboard=Keyboard(inline=True).add(Text("Топ дня по пополнениям", {"cmd": "top_pay"}), color=KeyboardButtonColor.PRIMARY).row().add(Text("Топ по рефералам", {"cmd": "top_ref"}), color=KeyboardButtonColor.PRIMARY))


@bot.on.private_message(payload={"cmd": "top_pay"})
async def top_pay_handler(message: Message):
    all_pays = dict()
    for payment in pays:
        all_pays[pays[payment]] = payment
    tt = ""
    num = 0
    max_pays = dict()
    for _ in range(len(all_pays) if len(all_pays) < 10 else 10):
        max_pays[max(all_pays)] = all_pays[max(all_pays)]
        del all_pays[max(all_pays)]
    for pay in max_pays:
        first_name = (await bot.api.users.get(max_pays[pay]))[0].first_name
        num += 1
        tt += f"{num}. [id{max_pays[pay]}|{first_name}]: Пополнил(-а) {pay} I$.\n\n"
        if num == 10:
            break
    await message.answer(f"Ежедневный топ по пополнениям:\n{tt}" if tt != "" else "Пока нету пополнений за сегодня...")


@bot.on.private_message(payload={"cmd": "top_ref"})
async def top_ref_handler(message: Message):
    uu = []
    rr = []
    for u in users:
        uu.append(u)
        rr.append(users[u]["ref"])
    tt = ""
    for nn in range(1, 11):
        m = max(rr)
        I = uu[rr.index(m)]
        first_name = (await bot.api.users.get(I))[0].first_name
        tt += f"{nn}. [id{I}|{first_name}]: Пригласил(-а) человек: {m}.\n\n"
        rr.remove(m)
        uu.remove(I)
    await message.answer(f"Топ по рефералам:\n{tt}" if tt != "" else "Топ по рефералам пока отсутствует...")


@bot.on.private_message()
async def default_handler(message: Message):
    ID = message.from_id
    info = await bot.api.users.get(ID)
    if ID not in users:
        create_account(ID)
        await message.answer(f"✅ Добро пожаловать в I$ Invest, {info[0].first_name}! Вы успешно зарегистрировались.\n\n🎁 Вам зачислено 3,000 I$ (3 ₽) на бонусный баланс за регистрацию в боте! На него можно купить виртуальный сервер.", keyboard=main_keyboard)
        try:
            int(message.ref)
            int(message.ref_source)
        except Exception:
            save()
            return
        if int(message.ref) in users and int(message.ref_source) == 1 and int(message.ref) != ID:
            users[ID]["bonusI$"] += 1000
            users[int(message.ref)]["bonusI$"] += 1500
            users[int(message.ref)]["ref"] += 1
            await message.answer(f"💰 Вы перешли по реферальной ссылке [id{message.ref}|пользователя] и получили за это +1000 I$ на бонусный баланс!")
            try:
                await bot.api.messages.send(peer_id=int(message.ref), message=f"🎉 По Вашей реферальной ссылке перешёл(-ла) [id{ID}|{info[0].first_name}], за это Вы получаете +1500 I$ на бонусный баланс!", random_id=0)
            except VKAPIError[901]:
                pass
        save()
        return
    
    elif users[ID]["action"] == "withdraw":
        try:
            text = message.text.split()
            if int(text[1]) < 10:
                await message.answer("🚫 Вывод на QIWI доступен от 10 ₽.")
                return
            if users[ID]["I$"] < 1500 * int(text[1]):
                await message.answer(f"🚫 Недостаточно I$ для вывода {text[1]} ₽.")
                return
            users[ID]["I$"] -= 1500 * int(text[1])
            total["RUB"] += int(text[1])
            save_total()
            save()
            await bot.api.messages.send(peer_id=owner, message=f"#Выводы\n@id{ID} вывел(а) {text[1]} ₽ на QIWI {text[0]}! Отправьте ему(-ей) средства на этот QIWI.", random_id=0)
            await message.answer(f"✅ Ваша заявка на вывод успешно принята.\nСумма вывода: {text[1]} ₽.\nНомер QIWI: {text[0]}.")
        except Exception:
            await message.answer("Что-то пошло не так...")
            return
    
    else:
        await message.answer("🚫 Команда не найдена.", keyboard=main_keyboard)
        return


@bot.on.chat_message(text=["Игра", "игра", "Рул", "рул", "Рулетка", "рулетка", "Казино", "казино"])
async def roulette_handler(message: Message):
    global rl
    if message.from_id not in users:
        create_account(message.from_id)
    tt = ""
    total = 0
    for n in rl:
        total += rl[n]["bid"]
    for r in rl:
        name = (await bot.api.users.get(int(r)))[0].first_name
        tt += f'[id{r}|{name}]: Ставка: {rl[r]["bid"]} I$ ({round(HMP(total, rl[r]["bid"]), 4)}%).\n'
    await message.answer(f'Игра «РУЛЕТКА»: Победитель забирает все деньги!\nВсе игроки в рулетке:\n{tt}' if tt != "" else "Игра «РУЛЕТКА»: Победитель забирает все деньги!\nПока нет игроков.", keyboard=Keyboard(inline=True).add(Text("Поставить", {"cmd": "rul_bid"}), color=KeyboardButtonColor.POSITIVE))


@bot.on.chat_message(payload={"cmd": "rul_bid"})
async def rul_bid_handler(message: Message):
    if message.from_id not in users:
        create_account(message.from_id)
    await message.answer("Отправьте Вашу ставку. Чем больше ставка, тем больше шансов выиграть!")
    users[message.from_id]["action"] = "chat_bid"


@bot.on.chat_message(text=".бал")
async def get_acc_handler(message: Message):
    if message.reply_message is not None:
        rID = message.reply_message.from_id
    else:
        rID = None
    ID = message.from_id
    if rID is not None and rID in users:
        await message.answer(f"👤 [id{rID}|{(await bot.api.users.get(rID))[0]. first_name}]:\n💰 I$: {users[rID]['I$']}.\n🎁 Бонусных I$: {users[rID]['bonusI$']}.\n📞 I$ Starter Server: {users[rID]['inventory']['I$ Starter Server']}.\n📱 I$ Mining Standart: {users[rID]['inventory']['I$ Mining Standart']}.\n💻 I$ Pro Server: {users[rID]['inventory']['I$ Pro Server']}.\n🖥️ I$ Station: {users[rID]['inventory']['I$ Station']}.")
    elif rID not in users and rID is not None:
        await message.answer("🚫 Пользователь не зарегистрирован в боте.")
    elif ID in users:
        await message.answer(f"👤 [id{ID}|{(await bot.api.users.get(ID))[0]. first_name}]:\n💰 I$: {users[ID]['I$']}.\n🎁 Бонусных I$: {users[ID]['bonusI$']}.\n📞 I$ Starter Server: {users[ID]['inventory']['I$ Starter Server']}.\n📱 I$ Mining Standart: {users[ID]['inventory']['I$ Mining Standart']}.\n💻 I$ Pro Server: {users[ID]['inventory']['I$ Pro Server']}.\n🖥️ I$ Station: {users[ID]['inventory']['I$ Station']}.")
    else:
        await message.answer("🚫 Вы не зарегистрированы в боте.")


@bot.on.chat_message()
async def chat_messags_handler(message: Message):
    global rl
    ID = message.from_id
    if message.from_id not in users:
        create_account(message.from_id)
    if users[ID]["action"] == "chat_bid":
        try:
            count = int(message.text)
            assert count > 0
        except Exception:
            await message.answer("🚫 Неправильный формат.")
            users[ID]["action"] = ""
            save()
            return
        if users[ID]["bonusI$"] >= count:
            users[ID]["bonusI$"] -= count
            if str(ID) not in rl:
                rl[str(ID)] = {"bid": count}
            else:
                rl[str(ID)]["bid"] += count
                users[ID]["action"] = ""
                save()
                open("JSON/Roulette.json", "w").write(dumps(rl))
                await message.answer(f"✅ Успешно прибавлена ставка в размере {count} I$ к Вашей ставке!")
                return
            await message.answer(f"✅ Успешно поставлено {count} I$!")
        elif users[ID]["I$"] >= count:
            users[ID]["I$"] -= count
            if str(ID) not in rl:
                rl[str(ID)] = {"bid": count}
            else:
                rl[str(ID)]["bid"] += count
                users[ID]["action"] = ""
                save()
                open("JSON/Roulette.json", "w").write(dumps(rl))
                await message.answer(f"✅ Успешно прибавлена ставка в размере {count} I$ к Вашей ставке!")
                return
            await message.answer(f"✅ Успешно поставлено {count} I$!")
        else:
            await message.answer("🚫 Недостаточно I$.")
            users[ID]["action"] = ""
            save()
            return
        users[ID]["action"] = ""
        save()
        open("JSON/Roulette.json", "w").write(dumps(rl))
        if len(rl) == 2:
            await asyncio.sleep(50)
            await message.answer("⌛ Итоги рулетки через 10 секунд!")
            await asyncio.sleep(10)
            total = 0
            for n in rl:
                total += rl[n]["bid"]
            num = randint(1, 1000000) / 10000
            total_t = 0
            for r in rl:
                if total_t < HMP(total, rl[r]["bid"]) + total_t > num:
                    name = (await bot.api.users.get(int(r)))[0].first_name
                    users[int(r)]["bonusI$"] += (total / 1.05) if not (total / 1.05).is_integer else int(total / 1.05)
                    await message.answer(f"🎉 Победитель рулетки: [id{r}|{name}]!\nСообщение о статистики Вашего выигрыша был выслан Вам в ЛС.")
                    try:
                        await bot.api.messages.send(peer_id=int(r), message=f"🎉 Вы выиграли рулетку!\n💵 Ваш выигрыш составляет: {total / 1.05 if not (total / 1.05).is_integer else int(total / 1.05)} I$.\nКомиссия: 5%.", random_id=0)
                    except VKAPIError[901]:
                        pass
                    rl = dict()
                    open("JSON/Roulette.json", "w").write(dumps(rl))
                    save()
                    return
                total_t += HMP(total, rl[r]["bid"])


@bot.on.raw_event(GroupEventType.GROUP_JOIN, dataclass=GroupTypes.GroupJoin)
async def group_join_handler(event: GroupTypes.GroupJoin):
    ID = event.object.user_id
    if ID in users:
        users[ID]["bonusI$"] += 1500
        save()
        try:
            await bot.api.messages.send(peer_id=ID, message="👥 Спасибо за подписку! Мы дарим Вам 1500 I$ на бонусный баланс.", random_id=0)
        except VKAPIError[901]:
            pass


@bot.on.raw_event(GroupEventType.GROUP_LEAVE, dataclass=GroupTypes.GroupLeave)
async def group_leave_handler(event: GroupTypes.GroupLeave):
    ID = event.object.user_id
    if ID in users:
        users[ID]["bonusI$"] -= 1500
        save()
        try:
            await bot.api.messages.send(peer_id=ID, message="👤 Из-за того, что Вы покинули нашу группу, мы вынуждены снять 1500 I$ с Вашего бонусного баланса...", random_id=0)
        except VKAPIError[901]:
            pass


@bot.on.raw_event(GroupEventType.LIKE_ADD, dataclass=GroupTypes.LikeAdd)
async def like_add_handler(event: GroupTypes.LikeAdd):
    ID = event.object.liker_id
    object = event.object.object_id
    obj_type = str(event.object.object_type)
    if ID in users and object not in users[ID]["likes"] and obj_type == "CallbackLikeAddRemoveObjectType.POST":
        users[ID]["bonusI$"] += 50
        users[ID]["likes"].append(object)
        save()
        try:
            await bot.api.messages.send(peer_id=ID, message="+50 I$ на бонусный баланс за лайк.", random_id=0)
        except VKAPIError[901]:
            pass


@bot.on.raw_event(GroupEventType.LIKE_REMOVE, dataclass=GroupTypes.LikeRemove)
async def like_remove_handler(event: GroupTypes.LikeRemove):
    ID = event.object.liker_id
    object = event.object.object_id
    obj_type = str(event.object.object_type)
    if ID in users and object in users[ID]["likes"] and obj_type == "CallbackLikeAddRemoveObjectType.POST":
        users[ID]["bonusI$"] -= 50
        users[ID]["likes"].append(object)
        save()
        try:
            await bot.api.messages.send(peer_id=ID, message="-50 I$ с бонусного баланса за удаление лайка.", random_id=0)
        except VKAPIError[901]:
            pass


bot.run_forever()
