import discord
from discord.ext import commands
import asyncio
import time
import logging
import os
import json
import re
from collections import deque, defaultdict
from dotenv import load_dotenv

# ====================== CL40 WORLD STREAM BOT ======================
TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"
ADMIN_IDS = [1315843947297509396, 1482904022695284808]

# Bot behaviour / anti-spam settings
COMMAND_PREFIX = "!"
SPAM_WINDOW = 60  # seconds to look back for spam
SPAM_THRESHOLD = 5  # number of commands in SPAM_WINDOW considered spam
MUTE_DURATION = 300  # seconds to ignore a spamming user

COOLDOWN_SECONDS = 30  # per-command cooldown for non-admins
COOLDOWN_TRACKER = defaultdict(dict)  # user_id -> {command_name: last_timestamp}

SPAM_TRACKER = defaultdict(deque)  # user_id -> deque[timestamps]
IGNORED_USERS = set()
EXEMPT_RUNTIME = {}  # runtime-exempt user IDs -> expiry timestamp (None = permanent)

# Professional features
COOLDOWN_SECONDS = 30  # per-command cooldown for non-admins
COOLDOWN_TRACKER = defaultdict(dict)  # user_id -> {command_name: last_timestamp}

# Channel restrictions: if non-empty, only these channels allow running commands
ALLOWED_CHANNELS = set()  # fill with channel IDs to restrict commands

# Optional audit channel ID (set to an int to enable posting audit logs)
AUDIT_CHANNEL_ID = None

SETTINGS_FILE = os.environ.get("BOT_SETTINGS_FILE", "settings.json")

def load_settings():
    global ALLOWED_CHANNELS, EXEMPT_RUNTIME
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                ALLOWED_CHANNELS = set(data.get("allowed_channels", []))
                EXEMPT_RUNTIME.clear()
                for k, v in data.get("exempt_runtime", {}).items():
                    EXEMPT_RUNTIME[int(k)] = v
                logger.info(f"Loaded settings from {SETTINGS_FILE}")
    except Exception:
        logger.exception("Failed to load settings")

def save_settings():
    try:
        data = {
            "allowed_channels": list(ALLOWED_CHANNELS),
            "exempt_runtime": {str(k): v for k, v in EXEMPT_RUNTIME.items()},
        }
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved settings to {SETTINGS_FILE}")
    except Exception:
        logger.exception("Failed to save settings")

# Logging setup
LOG_FILE = os.environ.get("BOT_LOG_FILE", "bot.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8"), logging.StreamHandler()],
)
logger = logging.getLogger("cl40world-bot")


async def audit_log(bot, message_text: str):
    logger.info(message_text)
    if AUDIT_CHANNEL_ID:
        try:
            ch = bot.get_channel(AUDIT_CHANNEL_ID)
            if ch:
                await ch.send(f"[Audit] {message_text}")
        except Exception:
            logger.exception("Failed to post audit message")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

def is_admin(ctx):
    return ctx.author.id in ADMIN_IDS or any(
        role.name.lower() in ["admin", "mod", "moderator"] for role in ctx.author.roles
    )


@bot.before_invoke
async def _track_and_maybe_mute(ctx):
    # Ignore if user is already muted
    uid = ctx.author.id
    now = time.time()

    # Ignore if user is already muted
    if uid in IGNORED_USERS:
        raise commands.CheckFailure("ignored")

    # Clean up expired runtime exemptions
    if uid in EXEMPT_RUNTIME:
        exp = EXEMPT_RUNTIME.get(uid)
        if exp is None:
            return
        if exp > now:
            return
        # expired
        del EXEMPT_RUNTIME[uid]

    # Exempt explicit ADMIN_IDS from spam limits and cooldowns
    if uid in ADMIN_IDS:
        return

    # Enforce allowed-channels policy (admins bypass)
    if ALLOWED_CHANNELS and getattr(ctx, "channel", None) and ctx.channel.id not in ALLOWED_CHANNELS:
        raise commands.CheckFailure("channel")

    # Enforce per-command cooldown (manual so admins can be exempt)
    cmd_name = ctx.command.name if ctx.command else None
    if cmd_name:
        last = COOLDOWN_TRACKER[uid].get(cmd_name, 0)
        if now - last < COOLDOWN_SECONDS:
            retry = int(COOLDOWN_SECONDS - (now - last))
            try:
                await ctx.send(f"⏳ رجاءً انتظر {retry} ثانية قبل إعادة استخدام هذا الأمر.")
            except Exception:
                pass
            raise commands.CheckFailure("cooldown")
        COOLDOWN_TRACKER[uid][cmd_name] = now

    now = time.time()
    dq = SPAM_TRACKER[uid]
    dq.append(now)
    # purge old timestamps
    while dq and now - dq[0] > SPAM_WINDOW:
        dq.popleft()

    if len(dq) > SPAM_THRESHOLD:
        IGNORED_USERS.add(uid)

        async def _unmute_later(u):
            await asyncio.sleep(MUTE_DURATION)
            IGNORED_USERS.discard(u)
            SPAM_TRACKER.pop(u, None)

        asyncio.create_task(_unmute_later(uid))
        try:
            await ctx.send("⚠️ لقد تم تجاهلك مؤقتًا بسبب الاستخدام المتكرر للأوامر. حاول مرة أخرى بعد بضع دقائق.")
        except Exception:
            pass
        raise commands.CheckFailure("ignored")


@bot.event
async def on_message(message):
    # Stay silent for bots and non-command messages
    if message.author.bot:
        return

    # Only react to messages that start with the command prefix
    if not message.content.startswith(COMMAND_PREFIX):
        return

    # If user is ignored, do nothing
    if message.author.id in IGNORED_USERS:
        return

    # Attachment blocking and URL filtering for non-admins/non-exempt
    uid = message.author.id
    is_exempt = uid in ADMIN_IDS or uid in EXEMPT_RUNTIME
    # attachments
    if message.attachments and not is_exempt:
        try:
            await message.channel.send("⚠️ المرفقات محجوبة للأوامر العادية. تواصل مع الإدارة إذا كنت تحتاج إرسال ملفات.")
        except Exception:
            pass
        return
    # simple URL detection
    if not is_exempt:
        if re.search(r"https?://|www\.", message.content):
            try:
                await message.channel.send("⚠️ الروابط محظورة داخل الأوامر لغير الإداريين.")
            except Exception:
                pass
            return

    await bot.process_commands(message)


def _parse_member_arg(ctx, arg: str):
    # Try to resolve member from mention, id, or name
    if not arg:
        return None
    if arg.isdigit():
        return ctx.guild.get_member(int(arg))
    if arg.startswith("<@") and arg.endswith(">"):
        try:
            mid = int(arg.strip("<@!>"))
            return ctx.guild.get_member(mid)
        except Exception:
            return None
    # fallback by name
    for m in ctx.guild.members:
        if m.name == arg or f"{m.name}#{m.discriminator}" == arg:
            return m
    return None

@bot.event
async def on_ready():
    print(f"✅ CL40 World Bot is online as {bot.user}")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="CL40 World Streams"
    ))

@bot.command()
async def golive(ctx):
    if not is_admin(ctx):
        return await ctx.send("❌ Only admins can use this command.")

    embed = discord.Embed(
        title="🔴 CL40 World is LIVE!",
        description="Chico Loco 40 & LB0025 are streaming right now!",
        color=0xFF0000
    )
    embed.add_field(name="📺 YouTube", value="[Watch Live](https://www.youtube.com/@chicoloco40)", inline=True)
    embed.add_field(name="📺 YouTube", value="[Watch Live](https://www.youtube.com/@lb0025-o6s)", inline=True)
    embed.add_field(name="🎮 KICK", value="[Watch Live](https://kick.com/chicoloco40live)", inline=True)
    embed.add_field(name="🌍 Official", value="[CL40 World](https://cl40.contact) | [Discord](https://discord.gg/H5cw3bexg)", inline=False)
    embed.set_footer(text="CL40 World • Powered by Grok • Sovereignty Mode ON")
    embed.timestamp = discord.utils.utcnow()

    await ctx.send(embed=embed)

# !stream - Public
@bot.command()
async def stream(ctx):
    await ctx.send(
        "🔴 **CL40 World LIVE**\n\n"
        "YouTube: https://youtube.com/@chicoloco40\n"
        "YouTube: https://youtube.com/@lb0025-o6s\n"
        "KICK: https://kick.com/chicoloco40live\n"
        "Official: https://cl40.contact"
    )


@bot.command(name="announce_album")
async def announce_album(ctx, *, payload: str):
    """Admin-only: announce an album release. Usage:
    !announce_album Title | https://store.link | Short note
    """
    if not is_admin(ctx):
        return await ctx.send("❌ عذرًا، ليس لديك الإذن لاستخدام هذا الأمر.")

    parts = [p.strip() for p in payload.split("|")]
    title = parts[0] if len(parts) > 0 else "New Release"
    url = parts[1] if len(parts) > 1 else None
    note = parts[2] if len(parts) > 2 else "Listen now!"

    embed = discord.Embed(title=f"🎵 {title}", description=note, color=0x1DB954)
    if url:
        embed.add_field(name="Listen / Buy", value=f"[Link]({url})", inline=False)
    embed.set_footer(text="CL40 World • Official Release")
    embed.timestamp = discord.utils.utcnow()

    try:
        await ctx.send(embed=embed)
        await audit_log(bot, f"{ctx.author} announced album: {title}")
    except Exception:
        await ctx.send("⚠️ فشل إرسال إعلان الألبوم.")


@bot.command(name="exempt")
async def exempt_user(ctx, member_arg: str, duration_days: str = None):
    """Admin-only: add a user to runtime admin exemptions (optional duration in days, default 3)."""
    if not is_admin(ctx):
        return await ctx.send("❌ عذرًا، ليس لديك الإذن لاستخدام هذا الأمر.")
    m = _parse_member_arg(ctx, member_arg)
    if not m:
        return await ctx.send("❌ لم أتمكن من إيجاد العضو.")
    if m.id in ADMIN_IDS:
        return await ctx.send("ℹ️ العضو إداري ومُعفى بالفعل.")

    # parse duration
    try:
        if duration_days is None:
            days = 3.0
        else:
            # allow '2.5' or '3' or '3d'
            s = duration_days.strip().lower()
            if s.endswith('d'):
                s = s[:-1]
            days = float(s)
    except Exception:
        return await ctx.send("❌ صيغة غير صحيحة للمدة. استعمل رقم الأيام مثل: `3` أو `2.5`.")

    now = time.time()
    expiry = now + int(days * 86400)
    EXEMPT_RUNTIME[m.id] = expiry
    await audit_log(bot, f"{ctx.author} added runtime-exempt for {m} ({m.id}) until {expiry}")
    await ctx.send(f"✅ تم إعفاء {m.mention} مؤقتًا لمدة {days} يوم(أ).")
    save_settings()


@bot.command(name="unexempt")
async def unexempt_user(ctx, member_arg: str):
    """Admin-only: remove a user from runtime admin exemptions."""
    if not is_admin(ctx):
        return await ctx.send("❌ عذرًا، ليس لديك الإذن لاستخدام هذا الأمر.")
    m = _parse_member_arg(ctx, member_arg)
    if not m:
        return await ctx.send("❌ لم أتمكن من إيجاد العضو.")
    if m.id not in EXEMPT_RUNTIME:
        return await ctx.send("ℹ️ العضو ليس لديه إعفاء مؤقت.")
    del EXEMPT_RUNTIME[m.id]
    await audit_log(bot, f"{ctx.author} removed runtime-exempt for {m} ({m.id})")
    await ctx.send(f"✅ تم إزالة الإعفاء المؤقت عن {m.mention}.")
    save_settings()


@bot.command(name="setchannel")
async def set_channel(ctx, channel: discord.TextChannel):
    """Admin-only: add a channel to allowed command channels."""
    if not is_admin(ctx):
        return await ctx.send("❌ عذرًا، ليس لديك الإذن لاستخدام هذا الأمر.")
    ALLOWED_CHANNELS.add(channel.id)
    await audit_log(bot, f"{ctx.author} added allowed channel #{channel.name} ({channel.id})")
    await ctx.send(f"✅ القناة {channel.mention} مسموح بها الآن للأوامر.")
    save_settings()


@bot.command(name="shutdown")
async def shutdown(ctx):
    if not is_admin(ctx):
        return await ctx.send("❌ عذرًا، ليس لديك الإذن لاستخدام هذا الأمر.")
    await audit_log(bot, f"{ctx.author} initiated shutdown")
    await ctx.send("🔌 جارٍ إيقاف البوت...")
    await bot.close()


@bot.event
async def on_command_error(ctx, error):
    # Polite handling of common errors
    if isinstance(error, commands.CommandOnCooldown):
        retry = int(error.retry_after)
        await ctx.send(f"⏳ رجاءً انتظر {retry} ثانية قبل إعادة استخدام هذا الأمر.")
    elif isinstance(error, commands.CheckFailure):
        # If it's the ignored check failure, remain quiet (already informed)
        if str(error) in ("ignored", "cooldown"):
            return
        if str(error) == "channel":
            # polite channel-restriction notice
            try:
                await ctx.send("🔒 هذا الأمر مسموح به فقط في القنوات المخصصة. تواصل مع فريق الإدارة إذا كنت تحتاج صلاحية.")
            except Exception:
                pass
            return
        await ctx.send("❌ عذرًا، ليس لديك الإذن لاستخدام هذا الأمر.")
    else:
        try:
            await ctx.send("⚠️ حدث خطأ بسيط. حاول مرة أخرى لاحقًا.")
        except Exception:
            pass
        print(f"Unhandled command error: {error}")

if __name__ == "__main__":
    if not TOKEN:
        logger.error("DISCORD_TOKEN is not set. Create a .env file with DISCORD_TOKEN=your_token or set the env var.")
        raise SystemExit("Missing DISCORD_TOKEN")
    load_settings()
    bot.run(TOKEN)
