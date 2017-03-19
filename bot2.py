import discord
import asyncio
import requests
import json
client = discord.Client()

with open('lastchannel') as f:
    lastchannel = f.read()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.send_message(lastchannel, 'Xenu is up and running! Commands begin with the prefix ! (but don\t be surprised if Xenu answers by himself)')

""" EXAMPLE CODE
counter = 0
tmp = await client.send_message(message.channel, 'Calculating messages...')
async for log in client.logs_from(message.channel, limit=100):
    if log.author == message.author:
        counter += 1

await client.edit_message(tmp, 'You have {} messages.'.format(counter))
"""

messageIndex = {
    'rickroll': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'xcq': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'it\'s time to stop': 'https://www.youtube.com/watch?v=2k0SmqbBIpQ',
    'stop': 'https://www.youtube.com/watch?v=2k0SmqbBIpQ'
}

containsMessageIndex = {
    # Returns the corresponding text if it contains the keyword unless it interferes with the pMI or mI
    'tommy wiseau' : 'do you mean one of the best actors in all of existance?'
    'determination' : 'Knowing the mouse might one day leave its hole and get the cheese... It fills you with determination.',
    'china' : 'https://www.youtube.com/watch?v=RDrfE9I8_hs',
    'tunak' : 'https://www.youtube.com/watch?v=vTIIMJ9tUc8',
    'tokyo' : 'https://www.youtube.com/watch?v=XxK54P_4PiA',
    'ghoul' : 'https://www.youtube.com/watch?v=XxK54P_4PiA',
    'nye' : 'https://www.youtube.com/watch?v=26OE9Bq-lr8',
    'yas' : 'https://www.youtube.com/watch?v=26OE9Bq-lr8',
    'taco' : 'https://www.youtube.com/watch?v=vZkjRVjge0g',
    'taco bell' : 'https://www.youtube.com/watch?v=vZkjRVjge0g',
    'senpai' : 'NOTICE ME SENPAI!!!! \nhttp://vignette4.wikia.nocookie.net/yandere-simulator/images/e/ea/Senpai_Sep18.png/revision/latest?cb=20150920021049',
    'jurassic' : 'https://www.youtube.com/watch?v=-w-58hQ9dLk',
    'my point' : 'https://www.youtube.com/watch?v=WOOw2yWMSfk',
    'shrek' : 'https://www.youtube.com/watch?v=cevWfNbRVpo',
    'america' : 'America is dead. All hail Trumpland.',
    'rump' : 'FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK https://www.youtube.com/watch?v=AtbMnixO2nc FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK RUMP'
}

@client.event
async def on_message(message):
    msg = message.content
    author = message.author
    channel = message.channel
    server = message.server
    #print('Xenu received message: "' + msg + '", said by user ' + str(author) + ' on channel ' + str(channel) + ' of server ' + str(server))
    if msg.startswith('!xenu'):
        await client.send_message(channel, 'Yes?')
    elif msg.startswith('!xkcd'):
        # Store the number/other content after the '!xkcd '.
        comic = msg[5:]
        # If the user included a specific comic number in their message, get the JSON data for that comic. Otherwise, get the JSON data for the most recent comic.
        r = requests.get('http://xkcd.com/' + comic + '/info.0.json' if comic else 'http://xkcd.com/info.0.json')
        # Send the URL of the image from the JSON fetched above.
        # The title text is half of the comic
        await client.send_message(channel, r.json()['img']+ '\n' + (r.json()['alt']))
    elif msg.startswith('!help') or msg.startswith('!about'):
        await client.send_message(channel, 'Xenu was the dictator of the Galactic Confederacy, who 75 million years ago brought billions of his people to Earth (then known as "Teegeeack") in DC-8-like spacecraft, stacked them around volcanoes, and killed them with hydrogen bombs. Bot is currently running as ' + client.user.name + ' (ID ' + client.user.id + '). View on GitHub: https://github.com/aderhall/xenu')
        await client.send_message(channel, 'Discuss Xenu at the Galactic Confederacy: https://discord.gg/aBT8hRT')
    elif msg.startswith('!invite'):
        await client.send_message(channel, 'Invite Xenu to your server with this link: https://discordapp.com/oauth2/authorize?client_id=' + str(client.user.id) + '&scope=bot&permissions=0\nNote: you must have *manage server* permissions on the server to add bots.')
    else:
        if msg in messageIndex:
            await client.send_message(message.channel, messageIndex[msg])
        else:
            for key, value in containsMessageIndex.items():
                if key in msg:
                    await client.send_message(message.channel, value)


@client.event
# Respond on a new member joining
async def on_member_join(member):
    await client.send_message(member.server.default_channel, '**Welcome ' + member.mention + ' to the ' + member.server.name + ' server! All Hail XENU**')

# Respond on member leaving
@client.event
async def on_member_remove(member):
    await client.send_message(member.server.default_channel, '**' + member.name + '\'s soul was captured and sucked into a vacuum zone. :frowning: Fuck **' + member.name)


with open('token.txt', 'r') as token_file:
    # Parse into a string, and get rid of trailing newlines
    token = token_file.read().replace('\n', '')
# It is only fair that whoever is running the bot should know their own token
print('Starting with token ' + token + '...')

# Start bot!
client.run(token)
