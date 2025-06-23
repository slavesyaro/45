import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Бот запущен как {bot.user}")

@bot.event
async def on_message(message):
    if message.guild is None and not message.author.bot:
        channel = bot.get_channel(int(os.getenv("CHANNEL_ID")))
        if channel:
            embed = discord.Embed(title="📩 Анонимное сообщение", description=message.content, color=0x00ffcc)
            await channel.send(embed=embed)
    await bot.process_commands(message)

@bot.command()
async def help(ctx):
    commands_list = """
**Доступные команды:**
!help — помощь
!ping — проверить связь
!report <текст> — отправить жалобу
!feedback <текст> — отправить обратную связь
!info — информация о боте
!rules — правила сервера
!delete <message_id> — удалить сообщение (модераторы)
"""
    await ctx.send(commands_list)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def report(ctx, *, message):
    channel = bot.get_channel(int(os.getenv("CHANNEL_ID")))
    if channel:
        embed = discord.Embed(title="📢 Анонимная жалоба", description=message, color=0xff5555)
        embed.set_footer(text="Отправлено через команду !report")
        await channel.send(embed=embed)
        await ctx.send("✅ Жалоба отправлена модераторам.")
    else:
        await ctx.send("1386462002221813872")

@bot.command()
async def feedback(ctx, *, message):
    feedback_channel = bot.get_channel(int(os.getenv("FEEDBACK_CHANNEL_ID")))
    if feedback_channel:
        embed = discord.Embed(title="📩 Анонимная обратная связь", description=message, color=0x55ff55)
        embed.set_footer(text="Отправлено через команду !feedback")
        await feedback_channel.send(embed=embed)
        await ctx.send("✅ Обратная связь отправлена.")
    else:
        await ctx.send("1386698428674867230")

@bot.command()
async def info(ctx):
    await ctx.send("Я — бот для анонимных сообщений и жалоб. Используй команды !help для списка команд.")

@bot.command()
async def rules(ctx):
    await ctx.send("Правила сервера: 1279828595505893446")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def delete(ctx, message_id: int):
    channel = bot.get_channel(int(os.getenv("CHANNEL_ID")))
    try:
        msg = await channel.fetch_message(message_id)
        await msg.delete()
        await ctx.send(f"✅ Сообщение {message_id} удалено.")
    except Exception as e:
        await ctx.send(f"⚠️ Не удалось удалить сообщение: {e}")

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
