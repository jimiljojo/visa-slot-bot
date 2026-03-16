import os
import io
from telethon import TelegramClient, events
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
GROUP_NAME = os.getenv("GROUP_NAME")
NOTIFY_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") #  # Direct chat ID - hardcoded 8218400068

logger.info(f"API_ID: {API_ID}")
logger.info(f"GROUP_NAME: {GROUP_NAME}")
logger.info(f"NOTIFY_CHAT_ID: {NOTIFY_CHAT_ID}")

client = TelegramClient('userbot_session', API_ID, API_HASH)

async def send_notification(message, photo_file=None):
    """Send notification to NOTIFY_CHAT_ID. Media from other chats is always downloaded
    and re-uploaded (never forwarded) so it works with protected chats."""
    try:
        # Always re-upload media from the monitored group: download to bytes then send.
        # This avoids "You can't forward messages from a protected chat" and ensures
        # every image (startup "last image" + all subsequent NewMessage images) is sent the same way.
        if photo_file is not None and not isinstance(photo_file, (str, bytes, io.IOBase)):
            try:
                logger.info("Downloading media to re-upload (no forwarding)...")
                data = await client.download_media(photo_file, file=bytes)
                if data:
                    buf = io.BytesIO(data)
                    buf.name = "image.jpg"
                    photo_file = buf
                else:
                    logger.error("Failed to download media; sending text only.")
                    photo_file = None
            except Exception as e:
                logger.error(f"Failed to download media; sending text only. Error: {e}")
                photo_file = None

        # Try different ways to send the message
        success = False
        
        # Method 1: Try with the chat ID as integer
        try:
            if photo_file:
                await client.send_file(NOTIFY_CHAT_ID, photo_file, caption=message)
            else:
                await client.send_message(NOTIFY_CHAT_ID, message)
            logger.info(f"Message sent successfully to chat ID {NOTIFY_CHAT_ID}")
            success = True
        except Exception as e:
            logger.error(f"Method 1 failed: {e}")
        
        # Method 2: Try with the chat ID as string
        if not success:
            try:
                if photo_file:
                    await client.send_file(str(NOTIFY_CHAT_ID), photo_file, caption=message)
                else:
                    await client.send_message(str(NOTIFY_CHAT_ID), message)
                logger.info(f"Message sent successfully to chat ID '{NOTIFY_CHAT_ID}'")
                success = True
            except Exception as e:
                logger.error(f"Method 2 failed: {e}")
        
        # Method 3: Try to get the user entity first
        if not success:
            try:
                user_entity = await client.get_entity(NOTIFY_CHAT_ID)
                logger.info(f"Found user: {user_entity.first_name} {user_entity.last_name or ''} (@{user_entity.username or 'no_username'})")
                
                if photo_file:
                    await client.send_file(user_entity, photo_file, caption=message)
                else:
                    await client.send_message(user_entity, message)
                logger.info("Message sent successfully using user entity")
                success = True
            except Exception as e:
                logger.error(f"Method 3 failed: {e}")
        
        if not success:
            logger.error("All methods failed to send notification")
            
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")

async def main():
    logger.info("Connecting...")
    await client.start()
    me = await client.get_me()
    logger.info(f"Connected as {me.username} ({me.id})")
    
    # Find the group entity by name
    try:
        group = await client.get_entity(GROUP_NAME)
        logger.info(f"Monitoring group: {group.title} ({group.id})")
    except Exception as e:
        logger.error(f"Failed to find group '{GROUP_NAME}': {e}")
        return

    # Test notification
    try:
        await send_notification("🤖 Telegram monitor is now running and listening for images!")
        logger.info("Test notification sent successfully")
    except Exception as e:
        logger.error(f"Failed to send test notification: {e}")
        return

    # Find and send the most recent image in the group's history (no message count limit)
    last_image_sent = False
    async for message in client.iter_messages(group):
        if message.photo:
            logger.info("Found last image in group, sending for testing...")
            try:
                await send_notification("🖼️ Last image from group (testing)", message.photo)
                logger.info("Last image sent successfully for testing")
                last_image_sent = True
            except Exception as e:
                logger.error(f"Failed to send last image: {e}")
            break
        elif message.file and message.file.mime_type and message.file.mime_type.startswith('image/'):
            logger.info(f"Found last image file in group, sending for testing...")
            try:
                await send_notification("🖼️ Last image from group (testing)", message.file)
                logger.info("Last image sent successfully for testing")
                last_image_sent = True
            except Exception as e:
                logger.error(f"Failed to send last image file: {e}")
            break
        elif message.text and not last_image_sent:
            logger.info(f"Last text message encountered before any image: '{message.text[:100]}' at {message.date}")
    
    if not last_image_sent:
        logger.info("No images found in group history for testing")

    @client.on(events.NewMessage(chats=group))
    async def handler(event):
        logger.info(f"New message received from {event.sender_id}")
        
        if event.photo:
            logger.info("Photo detected, forwarding...")
            try:
                await send_notification("🖼️ New image in group!", event.photo)
            except Exception as e:
                logger.error(f"Failed to forward photo: {e}")
        elif event.file and event.file.mime_type and event.file.mime_type.startswith('image/'):
            logger.info(f"Image file detected ({event.file.mime_type}), forwarding...")
            try:
                await send_notification("🖼️ New image in group!", event.file)
            except Exception as e:
                logger.error(f"Failed to forward image file: {e}")
        else:
            logger.info(f"Text or non-image message detected: '{event.text[:100] if event.text else 'No text'}' (not forwarded).")

    logger.info("Listening for images...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())