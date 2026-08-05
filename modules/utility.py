"""KurupDevs - Utility Module"""
import asyncio, string, random
from io import StringIO
from contextlib import redirect_stdout
import aiohttp
from pyrogram import Client, filters
from utils import modules_help, prefix
from utils.scripts import format_exc

@Client.on_message(filters.command(["sh", "shell"], prefix) & filters.me)
async def sh_cmd(_, message):
    if len(message.command) < 2:
        return await message.edit("<b>Specify command!</b>")
    cmd = message.text.split(maxsplit=1)[1]
    await message.edit(f"<b>$</b> <code>{cmd}</code>\n<b>Running...</b>")
    try:
        p = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        out, err = await asyncio.wait_for(p.communicate(), timeout=60)
        r = ""
        if out:
            r += f"<b>Out:</b>\n<code>{out.decode()[:2000]}</code>\n"
        if err:
            r += f"<b>Err:</b>\n<code>{err.decode()[:500]}</code>\n"
        r += f"<b>Exit:</b> <code>{p.returncode}</code>"
        await message.edit(f"<b>$</b> <code>{cmd[:500]}</code>\n{r[:3900]}")
    except asyncio.TimeoutError:
        await message.edit("<b>Timeout (60s)!</b>")
    except Exception as e:
        await message.edit(format_exc(e))

@Client.on_message(filters.command(["eval"], prefix) & filters.me)
async def eval_cmd(_, message):
    if len(message.command) < 2:
        return await message.edit("<b>No code!</b>")
    code = message.text.split(maxsplit=1)[1]
    try:
        result = eval(code)
        await message.edit(f"<b>Code:</b>\n<code>{code[:500]}</code>\n<b>Result:</b>\n<code>{str(result)[:2000]}</code>")
    except Exception as e:
        await message.edit(format_exc(e))

@Client.on_message(filters.command(["exec", "ex"], prefix) & filters.me)
async def exec_cmd(_, message):
    if len(message.command) < 2:
        return await message.edit("<b>No code!</b>")
    code = message.text.split(maxsplit=1)[1]
    out = StringIO()
    try:
        with redirect_stdout(out):
            exec(code)
        await message.edit(f"<b>Code:</b>\n<code>{code[:300]}</code>\n<b>Result:</b>\n<code>{out.getvalue()[:2000]}</code>")
    except Exception as e:
        await message.edit(format_exc(e))

@Client.on_message(filters.command(["whois", "info", "id"], prefix) & filters.me)
async def whois_cmd(client, message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user or message.reply_to_message.sender_chat
    elif len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except:
            try:
                user = await client.get_chat(message.command[1])
            except:
                return await message.edit("<b>Not found!</b>")
    else:
        user = message.from_user
    if hasattr(user, 'first_name'):
        t = f"<b>User:</b> {user.first_name} {user.last_name or ''}\n<b>ID:</b> <code>{user.id}</code>\n<b>@:</b> @{user.username or 'N/A'}"
    else:
        t = f"<b>Chat:</b> {user.title}\n<b>ID:</b> <code>{user.id}</code>"
    await message.edit(t)

@Client.on_message(filters.command(["tr", "translate"], prefix) & filters.me)
async def tr_cmd(_, message):
    if len(message.command) < 3 and not message.reply_to_message:
        return await message.edit(f"<b>Usage:</b> <code>{prefix}tr [lang] [text/reply]</code>")
    lang = message.command[1]
    txt = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[2:])
    if not txt:
        return await message.edit("<b>No text!</b>")
    await message.edit("<b>Translating...</b>")
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={lang}&dt=t&q={txt}") as r:
                d = await r.json()
        result = "".join(i[0] for i in d[0] if i[0])
        await message.edit(f"<b>Translated ({lang}):</b>\n<code>{result[:2000]}</code>")
    except Exception as e:
        await message.edit(format_exc(e))

@Client.on_message(filters.command(["weather"], prefix) & filters.me)
async def weather_cmd(_, message):
    if len(message.command) < 2:
        return await message.edit(f"<b>Usage:</b> <code>{prefix}weather [city]</code>")
    city = " ".join(message.command[1:])
    await message.edit(f"<b>Fetching weather...</b>")
    try:
        from utils.config import weather_api_key
        async with aiohttp.ClientSession() as s:
            async with s.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric") as r:
                d = await r.json()
        if d.get("cod") != 200:
            return await message.edit("<b>City not found!</b>")
        await message.edit(f"<b>{d['name']}:</b> {d['main']['temp']}C, {d['weather'][0]['description']}")
    except:
        await message.edit("<b>No API key configured!</b>")

@Client.on_message(filters.command(["currency"], prefix) & filters.me)
async def curr_cmd(_, message):
    if len(message.command) < 2:
        return await message.edit(f"<b>Usage:</b> <code>{prefix}currency [USD]</code>")
    await message.edit("<b>Fetching rates...</b>")
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(f"https://api.exchangerate-api.com/v4/latest/{message.command[1].upper()}") as r:
                d = await r.json()
        rates = {k: v for k, v in d.get("rates", {}).items() if k in ["USD","EUR","GBP","INR","JPY","PKR","BDT"] and k != message.command[1].upper()}
        txt = f"<b>{message.command[1].upper()} Rates:</b>\n" + "\n".join(f"<b>{k}:</b> {v}" for k, v in rates.items())
        await message.edit(txt)
    except Exception as e:
        await message.edit(format_exc(e))

@Client.on_message(filters.command(["qr"], prefix) & filters.me)
async def qr_cmd(client, message):
    txt = " ".join(message.command[1:]) if len(message.command) > 1 else (message.reply_to_message.text if message.reply_to_message else None)
    if not txt:
        return await message.edit(f"<b>Usage:</b> <code>{prefix}qr [text]</code>")
    try:
        await client.send_photo(message.chat.id, f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={txt}", caption="<b>QR Code</b>")
        await message.delete()
    except Exception as e:
        await message.edit(format_exc(e))

@Client.on_message(filters.command(["password", "passgen"], prefix) & filters.me)
async def pass_cmd(_, message):
    length = int(message.command[1]) if len(message.command) > 1 and message.command[1].isdigit() else 16
    pwd = "".join(random.choice(string.ascii_letters + string.digits + "!@#$%&") for _ in range(length))
    await message.edit(f"<b>Password:</b>\n<code>{pwd}</code>")

@Client.on_message(filters.command(["ip"], prefix) & filters.me)
async def ip_cmd(_, message):
    if len(message.command) < 2:
        return await message.edit(f"<b>Usage:</b> <code>{prefix}ip [address]</code>")
    await message.edit("<b>Looking up...</b>")
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(f"http://ip-api.com/json/{message.command[1]}") as r:
                d = await r.json()
        await message.edit(f"<b>IP:</b> {d['query']}\n<b>Country:</b> {d['country']}\n<b>City:</b> {d['city']}\n<b>ISP:</b> {d['isp']}")
    except Exception as e:
        await message.edit(format_exc(e))

@Client.on_message(filters.command(["google", "g"], prefix) & filters.me)
async def google_cmd(_, message):
    if len(message.command) < 2:
        return await message.edit(f"<b>Usage:</b> <code>{prefix}google [query]</code>")
    await message.edit(f"<b>Search:</b> https://www.google.com/search?q={'+'.join(message.command[1:])}")

@Client.on_message(filters.command(["speedtest", "speed"], prefix) & filters.me)
async def speedtest_cmd(_, message):
    await message.edit("<b>Running speedtest...</b>")
    try:
        import speedtest
        st = speedtest.Speedtest()
        st.get_best_server()
        d = st.download() / 1_000_000
        u = st.upload() / 1_000_000
        p = st.results.ping
        await message.edit(f"<b>Speed:</b> {d:.1f}Mbps down / {u:.1f}Mbps up / {p:.0f}ms")
    except ImportError:
        await message.edit("<b>speedtest-cli not installed!</b>")
    except Exception as e:
        await message.edit(format_exc(e))

modules_help["utility"] = {
    "sh [cmd]*": "Shell", "eval [code]*": "Python eval", "exec [code]*": "Python exec",
    "whois [user]": "User info", "id": "Get IDs", "tr [lang] [text]": "Translate",
    "weather [city]*": "Weather", "currency [code]*": "Rates",
    "qr [text]*": "QR Code", "password [len]": "Password gen",
    "ip [addr]*": "IP lookup", "google [query]*": "Google",
    "speedtest": "Speed test",
}
