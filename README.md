# Visa slot bot

I created this bot to getnotified when screenshots are available in the Telegram channel for dropbox appointments. 

How do I use this?

0. Clone this repo. Open your terminal and type `git clone https://github.com/jimiljojo/visa-slot-bot.git`. Once downloaded, `cd visa-slot=bot` to go inside the directory. 

1. Check python version (I used 3.9.7)
`python3 --version`

2. Create a new telegram app. https://my.telegram.org/apps - go here, login and create a new app. It should give you API ID and API Hash values

![image](https://user-images.githubusercontent.com/4116653/143096895-b1a29f9b-ea09-4f8e-9156-e90f1392f879.png)

3. In the python script add values for `api_hash` and `api_id`. From step #2

![image](https://user-images.githubusercontent.com/4116653/143068961-cb532e6d-1bc7-4777-b02e-a4f56eaf3a98.png)

4. Create a new telegram channel. Take a note of the username, and add it to the python script for `YOUR CHANNEL HERE` placeholder. This is where you will get screenshots forwarded to. 

5. Run the python script by typing `python3 tele_visa_script.py`. You will now get MacOS notification when a screenshot is available on the Dropbox channel with slots available. 

6. Keep script running. Install Telegram app on desktop. As soon as you get notification, start booking and dont give up. 

All the best, dont loose hope!!

