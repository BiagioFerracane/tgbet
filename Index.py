from telethon import TelegramClient, events
from telethon.tl.types import User, Chat, Channel 

# --- METTI QUI I TUOI VALORI ---
api_id = 33130141
api_hash = "47a49d737b9dc584dc427daed5868cc9"

# --- CREA IL CLIENT ---
client = TelegramClient("sessione.inoltro", api_id, api_hash)

# ID del gruppo da monitorare
GRUPPO_ID = [ -1001121869415 , -1002322369335 ]  # sostituisci con l'ID vero del gruppo

# username o ID del contatto destinatario
DESTINATARIO = -1003306350006 # o ID numerico come intero

@client.on(events.NewMessage(chats=GRUPPO_ID))
async def handler(event):
    try:
        chat = event.chat
        if isinstance(chat, (Chat, Channel)):
            nome_chat = chat.title
        elif isinstance(chat, User):
            nome_chat = chat.username or chat.first_name
        else:
            nome_chat = "Sconosciuto"

        print(f"Nuovo messaggio da {nome_chat}")

        await client.forward_messages(
            DESTINATARIO,
            event.message
        )
        print("Messaggio inoltrato!")

    except Exception as e:
        print("Errore nell'inoltro:", e)

# --- AVVIO CLIENT ---
client.start()
print("Script avviato... in ascolto dei messaggi del gruppo.")
client.run_until_disconnected()

