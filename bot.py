import discord
from discord.ext import commands

# ====================== CL40 WORLD STREAM BOT ======================
TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"
ADMIN_IDS = [1315843947297509396, 1482904022695284808]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

def is_admin(ctx):
    return ctx.author.id in ADMIN_IDS or any(
        role.name.lower() in ["admin", "mod", "moderator"] for role in ctx.author.roles
    )

@bot.event
async def on_ready():
    print(f"✅ CL40 World Bot is online as {bot.user}")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="CL40 World Streams"
    ))

# !golive - Admin only
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

bot.run(TOKEN)
