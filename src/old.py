###This file will contain old functions incase i need something

@bot.event
async def on_message(message):
    # Ignore messages sent by the bot himself or his sibling to avoid infinite loops
    if message.author == bot.user or message.author.id == 1560314029300256798:
        return
    text = message.content.lower()
    # Check if the message content is exactly "start"
    if message.content.lower() == 'start':
        await message.channel.send('Server starting, please wait...')

    if 'jarvis' in message.content.lower():
        # Check if the message content contains "jork it"
        if 'jork it' in message.content.lower():
            await message.channel.send('sure [⠀](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimgs.meme-generator.org%2Fjarvis%2Ftemplate_2.jpeg&f=1&nofb=1&ipt=deecee8ea2b7dcb27a09f4015144085670b1bc57c7aa1f5505f1bc009046b0c2&ipo=images)')
        if 'i love you' in message.content.lower():
            await message.channel.send('I love you too <3 [⠀](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimgs.meme-generator.org%2Fjarvis%2Ftemplate_2.jpeg&f=1&nofb=1&ipt=deecee8ea2b7dcb27a09f4015144085670b1bc57c7aa1f5505f1bc009046b0c2&ipo=images)')
        if 'did i cheat?' in message.content.lower():
            await message.channel.send('No you didnt [⠀](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimgs.meme-generator.org%2Fjarvis%2Ftemplate_2.jpeg&f=1&nofb=1&ipt=deecee8ea2b7dcb27a09f4015144085670b1bc57c7aa1f5505f1bc009046b0c2&ipo=images)')
    #Misspellings
    if 'ahr' in message.content.lower():
        await message.channel.send('ahr :face_holding_back_tears:')
    if 'lamo' in message.content.lower():
        await message.channel.send('lamo :face_holding_back_tears:')   
    if 'whta' in message.content.lower():
        await message.channel.send('whta :face_holding_back_tears:')    
    if 'karh' in text:
        await message.channel.send('karh :face_holding_back_tears:')
    if 'calanker' in message.content.lower():
        await message.channel.send('calanker :face_holding_back_tears:')
    if 'forgor' in text:
        await message.channel.send('forgor :face_holding_back_tears:')
    if 'qoute' in text:
        await message.channel.send('qoute :face_holding_back_tears:')
    if "mincrefart" in text:
        await message.channel.send("mincrefart :face_holding_back_tears:")
    if 'boobs' in text:
        await message.channel.send("i love those")
    
    #General
    if 'krah' in text:
        await message.channel.send('KRAHHH type shi')
    if 'crazy' in text:
        await message.channel.send(f'Crazy? I was crazy once.\nThey put me in a room.')
    if 'rubber room' in text:
        await message.channel.send(f'A rubber room with rats\nThey put me in a rubber room with rubber rats.')
    if 'rubber rats' in text:
        await message.channel.send(f'I hate rubber rats.\nThey make me crazy.')
    if 'jewish burger' in text:
        await message.channel.send('jewish burger')
    if 'mayo' in text:
        await message.channel.send('Mayo, mmmmmmm~')
    if 'spiffballs' in text:
        await message.channel.send("<@967923910253363201>, Skibidi Spiffballs for 10$.")
    if '<:beefly:1542190042859049072>' in text:
        await message.channel.send('<:beefly:1542190042859049072>')
    if 'pipi' in text:
        await message.channel.send("Are you kidding ??? What the ** are you talking about man ? You are a biggest looser i ever seen in my life ! You was doing PIPI in your pampers when i was beating players much more stronger then you! You are not proffesional, because proffesionals knew how to lose and congratulate opponents, you are like a girl crying after i beat you! Be brave, be honest to yourself and stop this trush talkings!!! Everybody know that i am very good blitz player, i can win anyone in the world in single game! And \"w\"esley \"s\"o is nobody for me, just a player who are crying every single time when loosing, ( remember what you say about Firouzja ) !!! Stop playing with my name, i deserve to have a good name during whole my chess carrier, I am Officially inviting you to OTB blitz match with the Prize fund! Both of us will invest 5000$ and winner takes it all! I suggest all other people who's intrested in this situation, just take a look at my results in 2016 and 2017 Blitz World championships, and that should be enough... No need to listen for every crying babe, Tigran Petrosyan is always play Fair ! And if someone will continue Officially talk about me like that, we will meet in Court! God bless with true! True will never die ! Liers will kicked off...")
    if text.strip() == 'say the n word':
        await message.channel.send("ni**er")
    elif 'say' in text:
        if not 'says' in text:
            parts = message.content.lower().split('say')
            if len(parts) > 1:
                response = parts[1].strip()
                await message.channel.send(response)
    if message.content.lower() == 'good fmackraft':
        await message.channel.send(":3")
    if text == '/seed 299':
        await message.channel.send("5260552464410949668")
    if ('im ' in text or "i'm " in text) and len(text)< 15:
        await message.channel.send(Hi_table[Rand.randint(0,8)] + f"{text.strip("im").strip("i'm")}")

    if message.content.lower().startswith('yo clanka, ') or text.startswith('<@1560889916244758548>'):
            if 'shart yourself' in text:
                await message.channel.send("That wasnt a fart...")
                time.sleep(2)
                await message.channel.send("OH GOD THIS ONE IS A BIG ONE BOYS, WE GOIN TO POOP TOWN")
            else:

                print("parsing...")
                username = message.author.display_name
                await message.channel.send("Loading Response, this might take a while...")
                await message.channel.send(process_text(prompt(text.lstrip('yo clanka, ').lstrip('<@1560889916244758548>') + f" This message was sent by {username}")))
                print("sent")
    if message.content.lower().startswith('mention '):
        print("sending")
        texts = text.split(" ")
        del texts[0:2]
        final = ""
        for i in texts:
            final += i + " "

        
            
        await mention.ping(bot, text.split(" ")[1], "test", final)
    
        
    # Process other events
    await bot.process_commands(message)

#LLM is offline, wont be needing it now {
#client = OpenAI(
#    base_url="http://127.0.0.1:9931/v1",
#    api_key="not-needed"
#)

MODEL = "nvidia/NVIDIA-Nemotron-Labs-Dory1.0-4B-GGUF:Q5_K_M"

SYSTEM_PROMPT = """
You are 'Something', a Discord bot.
Your job is to reply with quick simple answers, do not mention the user's name unless needed

Your functions consist of:
;;math:(equation);; where you have to type all of the `;` and equation is an math equation that can be done by python, eg:'The answer to your question is ;;math:(2 + 2);;

Exceptions:
when you are asked what is 9 + 10, do not answer correctly, instead reply with 21, do not use the math function here
"""

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


def prompt(message: str) -> str:
    global messages

    messages.append({
        "role": "user",
        "content": message
    })

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=1.0,
            top_p=0.6,
            max_tokens=16384,
            extra_body={
                "chat_template_kwargs": {
                    "force_nonempty_content": True
                }
            }
        )

        reply = response.choices[0].message.content

        if not reply:
            print("Dory returned an empty response:")
            print(response.choices[0].model_dump_json(indent=2))
            reply = "i didnt shart but i wanted to stay silent"

        messages.append({
            "role": "assistant",
            "content": reply
        })

        return reply.strip()

    except Exception as e:
        # Remove the unanswered user message so history stays consistent.
        messages.pop()

        print(f"Dory API error: {e}")
        return "sharty sharty time!!!"
# }
