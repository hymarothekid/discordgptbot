import discord
from discord.ext import commands
import g4f
import asyncio

intents = discord.Intents.all()

lock = asyncio.Lock()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def ask(ctx, *, question):
    async with lock:
        response = await bot.loop.run_in_executor(None, lambda: g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=[{"role": "user", "content": f"Você é uma bot amigável e você se chama Tess, e também não é minha ajudante só na programação, tente se apresentar menas vezes e seja mais objetiva! e não precisa dizer oi toda as vezes que o usuario enviar sua pergunta, e irá responder as pereguntas de um usuário com emojis e bem diretamente, tente ser companheira e amiga dele! aqui vai a pergunta dele: {question}"}],
        ))
    
        content = response
    
        import re
        content = re.sub(r'\[Source \d+\]\([^)]+\)', '', content)

        # Send the content to Discord
        if len(content) <= 4000:
            await ctx.send(content)
        else:
            with open('message_content.txt', 'w', encoding='utf-8') as file:
                file.write(content)
            
            await ctx.send("Essa mensagem está muito longa para mim enviar pelo discord! vou enviar txt viu! ☺", file=discord.File('message_content.txt'))

            import os
            os.remove('message_content.txt')
        
bot.run('change token here <3')
