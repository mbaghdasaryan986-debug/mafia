 -*- coding: utf-8 -*-
import telebot, threading, random, time, html
from telebot import types
import logging
telebot.logger.setLevel(logging.DEBUG)

TOKEN = "8575666142:AAF3gO6UqUtHKYYH5g9cRHzeZRlpX4IGX8o"

MIN_PLAYERS = 4          # նվազագույն խաղացողներ
MAX_PLAYERS = 20
LOBBY_TIME = 90          # վայրկյան՝ գրանցում
DAY_TIME = 90            # վայրկյան՝ քննարկում
VOTE_TIME = 45           # վայրկյան՝ քվեարկություն

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
games = {}               # chat_id -> Game

# ---------------- Դերեր ----------------
ROLES = {
    "civilian": ("👨 Խաղաղ բնակիչ", "Գտիր մաֆիային և քվեարկիր նրա դեմ ցերեկը:"),
    "mafia": ("🔪 Մաֆիա", "Քո պարտականությունն է ենթարկվել Դոնին ու սպանել բոլորին, ով կկանգնի քո ճանապարհին:"),
    "don": ("🤵 Դոն", "Դու մաֆիայի ղեկավարն ես: Ձայների հավասարության դեպքում քո ընտրությունն է վճռորոշ:"),
    "lover": ("💋 Սիրուհի", "Դու պետք է կենդանի մնաս այս դաժան աշխարհում: Օգտագործիր քո հմտությունները, որպեսզի վնասազերծես ցանկացած հերոսի մեկ օրով:)"),
    "doctor": ("🛡️ Թիկնապահ / Բժիշկ", "Աշխատանքը պարզ է՝ կանգնել հաճախորդի ու գնդակի միջև: Վատ են վճարում, բայց ազնիվ:"),
    "maniac": ("🔪 Մոլագար", "Քեզ շրջապատող բոլորը պետք է մեռնեն, բացի քեզնից իհարկե :)"),
    "commissar": ("🔍 Կոմիսար Կատտանի", "Ամեն գիշեր ստուգիր մեկին՝ պարզելու, թե նա մաֆիա է, թե ոչ:"),
    "lawyer": ("⚖️ Փաստաբան", "Գիշերը պաշտպանիր մաֆիայի անդամին: Կոմիսարին նա կերևա որպես խաղաղ բնակիչ:"),
    "journalist": ("📰 Լրագրող", "Գիշերը ընտրիր երկու խաղացողի՝ կիմանաս նրանք նույն թիմից են, թե ոչ:"),
    "sergeant": ("👮 Սերժանտ", "Դու Կոմիսարի օգնականն ես: Տեղեկանում ես նրա ստուգումներին, իսկ նրա մահվան դեպքում զբաղեցնում ես նրա տեղը:"),
}
MAFIA_TEAM = {"mafia", "don", "lawyer"}
ACTION_ROLES = {"lover", "doctor", "mafia", "don", "maniac", "commissar", "lawyer", "journalist"}


def team_of(role):
    if role in MAFIA_TEAM:
        return "mafia"
    if role == "maniac":
        return "maniac"
    return "peace"


class Game:
    def __init__(self, chat_id, host):
        self.host = host
        self.phase = "lobby"
        self.lobby_msg = None
        self.start_now = threading.Event()
        self.lock = threading.RLock()
        self.actions = {}
        self.jpick = {}
        self.done = set()
    def alive(self):
        return [u for u, p in self.players.items() if p["alive"]]
    return '<a href="tg://user?id=%d">%s</a>' % (uid, html.escape(g.players[uid]["name"]))
    except Exception as e:

    try:

    kb.add(types.InlineKeyboardButton("✅ Միանալ", callback_data="join"))
    return kb


@bot.message_handler(commands=["start"], chat_types=["private"])
def cmd_start(m):
    bot.send_message(m.chat.id, "Բարև 👋 Ես մաֆիայի բոտն եմ: Ավելացրու ինձ խմբում (ադմինի իրավունքներով) և գրիր /mafia")


@bot.message_handler(commands=["mafia"], chat_types=["group", "supergroup"])
def cmd_mafia(m):
    if m.chat.id in games:
        say(m.chat.id, "Խաղն արդեն ընթանում է կամ գրանցումը բաց է:")
        return
    g = Game(m.chat.id, m.from_user.id)
    games[m.chat.id] = g
    g.lobby_msg = say(m.chat.id, lobby_text(g), reply_markup=lobby_kb())
    threading.Thread(target=lobby_thread, args=(g,), daemon=True).start()


@bot.message_handler(commands=["startgame"], chat_types=["group", "supergroup"])
def cmd_stop(m):
    except Exception:
    if m.from_user.id == g.host or st in ("administrator", "creator"):
        g.event.set()
        if uid in g.players:
            return
        if len(g.players) >= MAX_PLAYERS:
            bot.answer_callback_query(c.id, "Տեղեր չկան")
            return
        try:  # ստուգում ենք՝ կարո՞ղ է բոտը գրել անձնականում
            bot.send_chat_action(uid, "typing")
        except Exception:
            bot.answer_callback_query(c.id, "Նախ բացիր բոտի հետ անձնական չաթը և սեղմիր START, հետո նորից միացիր:", show_alert=True)
        g.players[uid] = {"name": c.from_user.first_name or "Խաղացող", "role": None, "alive": True}
    bot.answer_callback_query(c.id, "Միացար ✅")
    g.start_now.wait(LOBBY_TIME)
    if g.stopped:
        games.pop(g.chat_id, None)
        return
    if len(g.players) < MIN_PLAYERS:
        say(g.chat_id, "❌ Բավարար խաղացող չկա (պետք է առնվազն %d): Խաղը չեղարկվեց:" % MIN_PLAYERS)
        games.pop(g.chat_id, None)
        return
    g.phase = "starting"
    run_game(g)


# ---------------- Դերերի բաշխում ----------------
def build_roles(n):
    roles = ["don", "commissar", "doctor"]
    for r, need in (("mafia", 7), ("lover", 8), ("maniac", 9), ("sergeant", 10), ("lawyer", 11), ("journalist", 12)):
        if n >= need:
            roles.append(r)
    while sum(1 for r in roles if r in MAFIA_TEAM) < max(1, n // 4) and len(roles) < n:
        g.players[uid]["role"] = r
    mafia_names = ", ".join(mention(g, u) for u in uids if g.players[u]["role"] in MAFIA_TEAM)
    for uid in uids:
        r = g.players[uid]["role"]
        txt = "Քո դերը՝ <b>%s</b>\n\n%s" % (ROLES[r][0], ROLES[r][1])
        if r in MAFIA_TEAM:
            txt += "\n\n🔪 Մաֆիայի թիմ՝ " + mafia_names
        say(uid, txt)


# ---------------- Խաղի ցիկլ ----------------
def run_game(g):
        assign_roles(g)
        say(g.chat_id, "🎭 Դերերը բաշխված են, ստուգեք անձնական նամակները: Խաղը սկսվում է!\n"
                       "Դերերի քանակ՝ " + ", ".join("%s ×%d" % (ROLES[r][0], n) for r, n in
                                                      count_roles(g).items()))
        games.pop(g.chat_id, None)


def count_roles(g):
    d = {}
    for p in g.players.values():
        d[p["role"]] = d.get(p["role"], 0) + 1
    return d


def target_kb(g, uid, prefix, exclude=()):
    kb = types.InlineKeyboardMarkup()
        if t in exclude:
            continue
        kb.add(types.InlineKeyboardButton(g.players[t]["name"], callback_data="%s:%d:%d" % (prefix, g.chat_id, t)))
    "journalist": "📰 Ընտրիր ԱՌԱՋԻՆ խաղացողին (հետո՝ երկրորդին):",
}


def night(g):
    g.phase = "night"
    g.actions, g.jpick, g.done = {}, {}, set()
    g.event = threading.Event()
    g.need = set(g.with_role(*ACTION_ROLES))
    say(g.chat_id, "🌙 <b>Գիշեր է.</b> Քաղաքը քնում է, մաֆիան արթնանում է...")
    set_chat_open(g, False)
    team = set(g.with_role(*MAFIA_TEAM))
    for uid in g.need:
        r = g.players[uid]["role"]
        if r in ("mafia", "don"):
            excl |= team
        if r == "lawyer":
            excl = set(u for u in g.alive() if u not in team or u == uid)
            if not (team - {uid}):
                g.need.discard(uid)
                continue
        say(uid, PROMPTS[r], reply_markup=target_kb(g, uid, "n", excl))
        g.event.wait(NIGHT_TIME)


def cb_night(c):
    uid, target = c.from_user.id, int(target)
    if not g or g.phase != "night" or uid not in g.need:
        return
    with g.lock:
        if uid in g.done:
            bot.answer_callback_query(c.id, "Արդեն ընտրել ես")
        if role == "journalist":
            g.actions[uid] = target
        if g.done >= g.need:
            g.event.set()
    bot.answer_callback_query(c.id, "Ընտրությունդ ընդունվեց ✅")
    try:
        bot.edit_message_text("✅ Ընտրությունդ ընդունվեց", c.message.chat.id, c.message.message_id)
    except Exception:
        pass


def kill_player(g, uid):
    p = g.players[uid]
    p["alive"] = False
    if p["role"] == "commissar":
        sgt = g.with_role("sergeant")
        if sgt:
            g.players[sgt[0]]["role"] = "commissar"
            say(sgt[0], "👮 Կոմիսարը մահացավ: Դու այժմ <b>🔍 Կոմիսար</b> ես:")
    set_dead_note(g, uid)


def set_dead_note(g, uid):
    say(uid, "💀 Դու դուրս մնացիր խաղից: Խնդրում ենք չգրել չաթում մինչև խաղի ավարտը:")

def resolve_night(g):
    A, P = g.actions, g.players
    blocked = None
    for u in g.with_role("lover"):
        if u in A:
        say(blocked, "💋 Այս գիշեր քեզ զբաղեցրին, քո գործողությունը չեղարկվեց:")
    for u in g.with_role("mafia", "don"):
        if ok(u):
            tally[A[u]] = tally.get(A[u], 0) + 1
            if P[u]["role"] == "don":
                don_vote = A[u]
    mafia_target = None
    if tally:
        best = [t for t, v in tally.items() if v == top]

    protected = None
        if ok(u):
        if ok(u):
        if t is None or t in deaths:
            saved = True
        else:

    for u in g.with_role("commissar"):
            res = "🔪 Մաֆիա" if is_m else "👨 Խաղաղ բնակիչ"
            say(u, "🔍 %s — %s" % (mention(g, t), res))
            for s in g.with_role("sergeant"):
            say(u, "📰 %s և %s՝ %s" % (mention(g, a), mention(g, b),
            say(u, "🛡️ Այս գիշեր դու մեկին փրկեցիր մահից:")
    txt = "☀️ <b>Առավոտ է.</b>\n"
            kill_player(g, t)
    say(g.chat_id, txt)
        (DAY_TIME, "\n".join("• " + mention(g, u) for u in alive)))
    for t in g.votes.values():
def vote_phase(g):
        kb.add(types.InlineKeyboardButton(g.players[t]["name"], callback_data="v:%d:%d" % (g.chat_id, t)))
    if not cnt:
        say(g.chat_id, "Ոչ ոք չքվեարկեց, այսօր ոչ ոք չի կախվում:")
        return
@bot.callback_query_handler(func=lambda c: c.data.startswith("v:"))
    uid, target = c.from_user.id, int(target)
    g.votes[uid] = target
    elif man and m == 0 and len(alive) <= 2:
        res = "🏆 <b>Մոլագարը հաղթեց!</b>"
    elif m and m >= len(alive) - m:
        res = "🏆 <b>Մաֆիան հաղթեց!</b>"
    if not res:
        return False
    roles = "\n".join("%s — %s %s" % (html.escape(p["name"]), ROLES[p["role"]][0], "" if p["alive"] else "💀")
                      for p in g.players.values())
    say(g.chat_id, res + "\n\nԴերերը:\n" + roles)
    return True

# Մահացածների հաղորդագրությունները ջնջվում են
@bot.message_handler(func=lambda m: m.chat.id in games, content_types=["text"])
def guard(m):
except Exception as e:
    print("ՏՈԿԵՆԻ ՍԽԱԼ:", e)
print("Բոտը աշխատում է...")
bot.infinity_polling(skip_pending=True)
