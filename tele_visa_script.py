from telethon import TelegramClient, events, sync
import os

#get this by creating a new bot. Message BotFather with /newbot request
api_id = API_ID_HERE
api_hash = 'YOUR API HASH'
client = TelegramClient('anon', api_id, api_hash)

#This function creates a notification on MacOS when the python script is running
def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

#This function listens for new messages in the dropbox channel. You can change it to the VAC channel if you want
@client.on(events.NewMessage(chats='H1B_H4_Visa_Dropbox_slots'))    #select channel you want to monitor
async def my_event_handler(event):
    if event.photo:
        notify("image -", event.raw_text)
        await client.send_message(entity=entity,message=event.message)

client.start()
entity=client.get_entity('YOUR CHANNEL HERE')  #channel you want to forward screenshots to
client.run_until_disconnected()