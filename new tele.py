import requests
import telepot
from bs4 import BeautifulSoup
BOT_TOKEN = "6856450947:AAFOacFQ7TrLxd3im1B-4F3_W2usiWmz5bQ"
CHANNEL_ID = -1002027065178
def get_image_urls_with_captions(url):
    image_data = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        image_tags = soup.find_all("img")
        for img in image_tags:
            src = img.get("src")
            if src:
                if not src.startswith("http"):
                    src = url + src.lstrip("/")
                # Exclude images with a specific URL (e.g., the logo)
                if "https://ethiopia-e-visa.com/images/logo.png" not in src:
                 if "https://ethiopia-e-visa.com/images/ajax-loader4.gif" not in src:
                    caption = img.get("alt", "") 
                    image_data.append({"url": src, "caption": caption})
    except Exception as e:
        print(f"Error fetching image URLs: {e}")
    return image_data
def send_images(chat_id, channel_id, image_urls, captions):
    try:
        bot = telepot.Bot(BOT_TOKEN)
        for i, image_url in enumerate(image_urls):
            bot.sendPhoto(chat_id, photo=image_url, caption=captions[i])
            bot.sendPhoto(channel_id, photo=image_url, caption=captions[i])
        print("Images sent successfully!")
    except Exception as e:
        print(f"Error sending images: {e}")
def handle_start_command(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == "text" and msg["text"] == "/command1":
        website_url = "https://ethiopia-e-visa.com/10-photogenic-spots-in-ethiopia/"
        image_data = get_image_urls_with_captions(website_url)
        if image_data:
            image_urls = [entry["url"] for entry in image_data]
            captions = [entry["caption"] for entry in image_data]
            send_images(chat_id, CHANNEL_ID, image_urls, captions)
        else:
            print("No images found on the website.")
if __name__ == "__main__":
    bot = telepot.Bot(BOT_TOKEN)
    bot.message_loop(handle_start_command)
    print("Listening for /start command...")
    while True:
        pass
