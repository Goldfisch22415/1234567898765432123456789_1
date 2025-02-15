import os
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ROLE_ID = 1335535087587954738

@bot.event
async def on_ready():

    await bot.tree.sync()
    print(f"Bot ist online als {bot.user}")

@bot.event
async def on_member_join(member: discord.Member):
    """Erstellt für jedes neue Mitglied einen privaten Kanal und sendet eine Willkommensnachricht."""
    guild = member.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True)
    }
    channel = await guild.create_text_channel(name=f"welcome-{member.name}", overwrites=overwrites)

    await channel.send(
        f"**Herzlich willkommen** auf **GameHUB**, {member.mention}.\n\n"
        "Wir freuen uns, dich hier begrüßen zu dürfen! Bitte nimm dir einen Moment Zeit, die Regeln durchzulesen, \n"
        "damit wir gemeinsam eine freundliche und respektvolle Community aufbauen können.\n\n"
        "**Schreibe `/accept`, um die Regeln zu akzeptieren und dem Server beizutreten.**"
    )

@bot.tree.command(name="accept", description="Akzeptiere die Regeln und erhalte die Mitgliedsrolle.")
async def accept(interaction: discord.Interaction):
    """Slash-Command, mit dem das Mitglied die Regeln akzeptiert, die Rolle erhält und der Kanal gelöscht wird."""
    member = interaction.user  
    guild = interaction.guild

    role = guild.get_role(ROLE_ID)
    if role is None:
        await interaction.response.send_message("Fehler: Die Rolle existiert nicht!", ephemeral=True)
        return

    try:
        await member.add_roles(role)
    except discord.Forbidden:
        await interaction.response.send_message("Keine Berechtigung, um die Rolle zu vergeben!", ephemeral=True)
        return

    await interaction.response.send_message(f"{member.mention}, du bist jetzt Mitglied!🎉")

    await asyncio.sleep(2)

    try:
        await interaction.channel.delete()
    except discord.Forbidden:
        print("Fehler: Keine Berechtigung, um den Kanal zu löschen.")
    except discord.HTTPException as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
    
#twichtig für alles
from flask import Flask
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "OK", 200  # Antwort für den Health-Check

def run_webserver():
    app.run(host="0.0.0.0", port=8000)

# Starte den Webserver in einem eigenen Thread
threading.Thread(target=run_webserver, daemon=True).start()

bot.run(os.getenv("DISCORD_TOKEN"))
