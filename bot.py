import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env (opcional)
load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", 0))  # ID do teu servidor
ROLE_SARGENTO_ID = int(os.getenv("DISCORD_ROLE_SARGENTO_ID", 0))  # role autorizada
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8000/frontend/index.html")  # URL do frontend

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot ligado como {bot.user}")
    guild = discord.Object(id=GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    print("Slash commands sincronizados.")

# -----------------------------
# COMANDO /avaliacoes
# -----------------------------
@app_commands.command(name="avaliacoes", description="Abrir formulário de avaliação")
async def avaliacoes(interaction: discord.Interaction):
    # Verificar se o utilizador tem a role correta
    member = interaction.guild.get_member(interaction.user.id)
    if not any(role.id == ROLE_SARGENTO_ID for role in member.roles):
        return await interaction.response.send_message(
            "❌ Não tens permissão para usar este comando.", ephemeral=True
        )

    user_id = interaction.user.id

    # Gerar URL do formulário com o user_id como parâmetro
    url = f"{FRONTEND_URL}?user_id={user_id}"

    embed = discord.Embed(
        title="📋 Avaliação de Guarda",
        description="Clique no botão abaixo para abrir o formulário.",
        color=0x2b2d31
    )

    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Abrir formulário", url=url))

    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

bot.tree.add_command(avaliacoes)

bot.run(TOKEN)
