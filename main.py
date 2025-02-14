import os
import discord
from discord.ext import commands
import asyncio

DISCORD_TOKEN={{ secret.DISCORD_TOKEN }}


# Erforderliche Intents aktivieren (wichtig für Nachrichten-Events)
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Notwendig, um Nachrichten zu lesen

# Erstelle den Bot; der command_prefix ist hier optional, da wir Slash-Commands verwenden.
bot = commands.Bot(command_prefix="!", intents=intents)

# Die ID der Rolle, die vergeben werden soll
ROLE_ID = 1335535087587954738

@bot.event
async def on_ready():
    # Synchronisiere die Anwendungskommandos (Slash-Commands)
    await bot.tree.sync()
    print(f"Bot ist online als {bot.user}")

@bot.event
async def on_member_join(member: discord.Member):
    """Erstellt für jedes neue Mitglied einen privaten Kanal und sendet eine Willkommensnachricht."""
    guild = member.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),  # Standardrolle hat keinen Zugriff
        member: discord.PermissionOverwrite(read_messages=True)  # Nur das neue Mitglied kann lesen
    }
    # Erstelle einen privaten Textkanal
    channel = await guild.create_text_channel(name=f"welcome-{member.name}", overwrites=overwrites)

    # Sende die Willkommensnachricht im Kanal
    await channel.send(
        f"**Herzlich willkommen** auf **{server_name}**, {member.mention}.\n\n"
        "Wir freuen uns, dich hier begrüßen zu dürfen! Bitte nimm dir einen Moment Zeit, die Regeln durchzulesen, "
        "damit wir gemeinsam eine freundliche und respektvolle Community aufbauen können.\n\n"
        "**Schreibe `/accept`, um die Regeln zu akzeptieren und dem Server beizutreten.**"
    )

@bot.tree.command(name="accept", description="Akzeptiere die Regeln und erhalte die Mitgliedsrolle.")
async def accept(interaction: discord.Interaction):
    """Slash-Command, mit dem das Mitglied die Regeln akzeptiert, die Rolle erhält und der Kanal gelöscht wird."""
    member = interaction.user  # Das Mitglied, das den Befehl ausführt
    guild = interaction.guild

    # Rolle anhand der ID abrufen
    role = guild.get_role(ROLE_ID)
    if role is None:
        await interaction.response.send_message("Fehler: Die Rolle existiert nicht!", ephemeral=True)
        return

    # Rolle dem Mitglied zuweisen
    try:
        await member.add_roles(role)
    except discord.Forbidden:
        await interaction.response.send_message("Keine Berechtigung, um die Rolle zu vergeben!", ephemeral=True)
        return

    # Bestätigungsnachricht senden
    await interaction.response.send_message(f"{member.mention}, du bist jetzt Mitglied! 🎉")

    # Kurze Wartezeit, damit die Bestätigung gelesen werden kann
    await asyncio.sleep(2)

    # Versuche, den Kanal zu löschen, in dem der Befehl ausgeführt wurde
    try:
        await interaction.channel.delete()
    except discord.Forbidden:
        print("Fehler: Keine Berechtigung, um den Kanal zu löschen.")
    except discord.HTTPException as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

# Starte den Bot, indem das Token aus der Umgebungsvariable 'DISCORDTOKEN' geladen wird.

bot.run("DISCORD_TOKEN")
