from venv import create

import discord
import asyncio
from discord.ext import commands
from discord import app_commands
import os
from langchain_groq import ChatGroq


intents = discord.Intents.all()
bot = commands.Bot("/", intents=intents)

# Mwnsagem ao ligar o bot
@bot.event
async def on_ready():
    print("Bot pronto para uso...")
# ------------------------------------

#Comando /ola
@bot.command()
async def ola(ctx):
    nome = ctx.author.display_name
    await ctx.reply(f"olá {nome} Como voce está? Use /helpp para saber os comandos")
# -----------------------------------------------------------------------------------

#/helpp de membro
@bot.command()
async def helpp(ctx):
    await ctx.reply("Click no botão verde em #https://discord.com/channels/1399318141053702204/1401296463438549125 pra tentar entrar na melhor org!")
#-----------------------------------------------------------------------------------------------------------------------------------------------------

# FORMULARIO
class FormularioButton(discord.ui.View):
    @discord.ui.button(label="Click para criar um formulário", style=discord.ButtonStyle.green)
    async def  criar_formulario(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        usuario = interaction.user

        nome_canal = f"formulario-{usuario.display_name}".replace(" ", "-")

        overwrites = {}
        for role in guild.roles:
            if not role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(read_messages=False)
        overwrites[usuario] = discord.PermissionOverwrite(read_messages=True)

        canal = await guild.create_text_channel(nome_canal, overwrites=overwrites)

        await canal.send("### responda as perguntas abaixo para concluir seu formulario!")

        await interaction.response.send_message(
            f"✅ {usuario.mention}, seu formulário foi criado: {canal.mention}",
            ephemeral=True
        )
        perguntas = ["Seu nome occ 1/12", "Sua idade occ 2/12", "Nick ic 3/12", "Rg in game 4/12", "Level 5/12", "Qualidades 6/12", "Estuda/trabalha? 7/12", "Já foi de org/corp? 8/12", "vai cumprir metas? 9/12", "Mobile ou pc? 10/12", "print do rg frente verso 11/12 " ]
        respostas = []

        pergunta_msg = await canal.send(perguntas[0])
        i = 0

        def check(msg):
            return msg.author == usuario and msg.channel == canal

        while i < len(perguntas):
            msg = await interaction.client.wait_for("message", check=check)
            respostas.append(msg.content)
            await msg.delete()

            i += 1
            if i < len(perguntas):
                await pergunta_msg.edit(content=perguntas[i])
            else:
                await pergunta_msg.edit(content="✅ Formulário finalizado! Obrigado pelas respostas.")
        await asyncio.sleep(5)
        await canal.delete()
        log_channel = discord.utils.get(guild.text_channels, name="『📋』respostas")  # Nome do canal de destino
        if log_channel:
            texto = f"# 📋 **Formulário de {usuario.display_name}**\n\n"
            for i in range(len(perguntas)):
                texto += f"**{i + 1}. {perguntas[i]}**\n{respostas[i]}\n\n"
            await log_channel.send(f"📋 **Formulário de {usuario.mention}:**\n{texto}")
@bot.command()
async def criar_formulario(ctx):
    view = FormularioButton()
    await ctx.send("Clique no botão abaixo para criar seu formulario:", view=view)
#------------------------------------------------------------------------------------------------------

#Pedir cartao
class cartaoButton(discord.ui.View):
    @discord.ui.button(label="click para criar cartao de metas ", style=discord.ButtonStyle.green)
    async def solicitar_cartao(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        usuario = interaction.user
        nome_do_cartao = (f"💳┇{usuario.name}")
        perguntas = [f"Qual seu nick ic? ", "Qual seu rg IC?"]
        respostas = []
        overwrites = {}
        for role in guild.roles:
            if not role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(read_messages=False)
        overwrites[usuario] = discord.PermissionOverwrite(read_messages=True)
        canal = await guild.create_text_channel(nome_do_cartao, overwrites=overwrites)
        await interaction.response.send_message(
            f"✅ {usuario.mention}, sua solicitação foi criada: {canal.mention}",
            ephemeral=True)
        pergunta_msg = await canal.send(perguntas[0])
        i = 0

        def check(msg):
             return msg.author == usuario and msg.channel == canal

        while i < len(perguntas):
            msg = await interaction.client.wait_for("message", check=check)
            respostas.append(msg.content)
            await msg.delete()

            i += 1
            if i < len(perguntas):
                await pergunta_msg.edit(content=perguntas[i])
            else:
                await pergunta_msg.edit(content="✅ Cartao finalizado! Obrigado pelas respostas.")
                # categoria = discord.utils.get(guild.categories, name="『💳』 ᴄᴀʀᴛõᴇs")
                # cartao_nome = f"💳┇{respostas[0, 1]}".replace(" ", "-")
                # cartao = await guild.create_text_channel(cartao_nome, overwrites=overwrites, category=categoria)
                await asyncio.sleep(5)
                await canal.delete()
        categoria = discord.utils.get(guild.categories, name="『💳』 ᴄᴀʀᴛõᴇs")
        cartao_nome = f"💳┇{respostas[0]}-{respostas[1]}".replace(" ", "-")
        cartao = await guild.create_text_channel(cartao_nome, overwrites=overwrites, category=categoria)
        await cartao.send("""FORMA CORRETA DE BATER CARTAO!

            50k de materiais

            NICK

            RG

            QUANTIDADE MATERIAIS 

            QUANTIDADE MACONHA

            @everyone @here""",

        )
        await interaction.followup.send(
            f"✅ {usuario.mention}, seu cartao foi criado: {canal.mention}",
                ephemeral=True
        )
@bot.command()
async def solicitar_cartao(ctx):
    view = cartaoButton()
    await ctx.send("Clique no botão abaixo para criar seu cattão de metas:", view=view)

@bot.command()
async def Lockk(ctx):
    canal = ctx.channel
    everyone = ctx.guild.default_role
    await canal.set_permissions(everyone, send_messages=False)
    await canal.send(f"Canal {canal.mention} bloqueado com sucesso! {ctx.author.mention}")

@bot.command()
async def unlock(ctx):
    canal = ctx.channel
    everyone = ctx.guild.default_role
    await canal.set_permissions(everyone, send_messages=True)
    await canal.send(f"Canal {canal.mention} desbloqueado com sucesso! {ctx.author.mention}")
@bot.command()
async def commandss(ctx):
    quantidade = len(bot.commands)
    await ctx.send(f" O bot tem **{quantidade}** comandos registrados!")


chat = ChatGroq(model='openai/gpt-oss-20b')

@bot.command()
async def perguntar(ctx, *, pergunta):
    await ctx.reply("pensando...")
    if "modelo" in pergunta.lower():
        await ctx.reply("Eu sou o modelo Vent Ia, desenvolvido especialmente para esse projeto!!!")
        return
    resposta = chat.invoke(pergunta)
    await ctx.reply(resposta.content)


@bot.command()
async def limpar(ctx, quantidade_de_mensagens: int):
    if quantidade_de_mensagens < 2:
        await ctx.reply("❌ Digite um número válido (maior que 0).")
        return

    await ctx.channel.purge(limit=quantidade_de_mensagens)
    await ctx.send(f"🧹 Apaguei {quantidade_de_mensagens} mensagens!")


@bot.command()
async def list_commandss(ctx):
    lista = [f"/{cmd.name}" for cmd in bot.commands]
    comandos = "\n".join(lista)
    await ctx.send(f"🧠 **Lista de comandos disponíveis:**\n{comandos}")


# Para rodar o BOT, precisa de uma API_KEY para acessar chatgpt chamada "GROQ_API_KEY"
BOT_TOKEN = getenv("BOT_TOKEN")
bot.run(BOT_TOKEN)
