# To run: from folder type python3 launch.py
# Work In Progress: will give many debug messages as it runs

# Must be run with python3 3.5 or higher
# Works with tmux sessions (highly recommended)
# Requires write access to local folder for persistent logs of some data
# Will not work on a read-only filesystem
# Can run as standard level user
# Tested on Mac OSX El Capitan 10.11.5, Lubuntu 16.04 LTS 64 and Ubuntu 16.10 (GNU/Linux 4.8.0-22-generic x86_64)
# Should in theory work on Windows computers as well

# Import various libraries
# Requires all of these except lxml for now, because the VPS hosting it has some problems with dpkg and tex-common (NOTE: I have identified these as part of the high-priority Ubuntu bug #1236951)
import discord
import asyncio
import subprocess
import requests
import json
import os
import itertools
import lxml
import time
import random
from discord.ext import commands
description = '''A bot for FRC team 1418's discord server. Still a work in progress, please make a pull request with any suggestions'''
bot = commands.Bot(command_prefix='!', description=description)
# Adaptable function for searching through text
def contains(origin, text):
    vf = False
    soc = 0
    i = -1
    loop = True
    while loop:
        vf = False
        i += 1
        if origin[i] == text[0]:
            a = -1
            loop2 = True
            while loop2:
                a += 1
                try:
                    if origin[a+i] != text[a]:
                        vf = True
                except:
                    vf = True
                if a >= (len(text)-1):
                    loop2 = False
        else:
            vf = True
        if vf == False:
            soc += 1
        if i >= (len(origin)-1):
            loop = False
            vf = True
    return soc
def replace(origin, char, newchar):
    actext = ''
    for thechar in origin:
        if thechar == char:
            actext = actext + newchar
        else:
            actext = actext + thechar
    return actext

# Initialize bot client
# TODO: Make bot a class like normal bots.
client = discord.Client()
# Load saved data from previous instances
lastchannel = str(subprocess.Popen('cat lastchannel', shell=True, stdout=subprocess.PIPE).stdout.read())
print (lastchannel)
lastuser = lastchannel[22:]
lastuser = lastuser[:-7]
lastchannel = lastchannel[2:20]
lasttime = str(subprocess.Popen('cat lasttime', shell=True, stdout=subprocess.PIPE).stdout.read())
lasttime = lasttime[2:-3]
print (lastuser)
print (lastchannel)
# Bot prefix
PREFIX = '!'

# Three dictionaries (prefix commands and text triggers) of basic things for the bot to return. More complex (i.e.
# data-driven) interactions aren't stored here, those go below.
prefixMessageIndex = {
    # Returns the corresponding value if preceeded by the PREFIX
    PREFIX + 'ping': 'Pong!',
    PREFIX + 'hello': 'World!',
    PREFIX + 'balloumoji': '<:bigdissapointment:236086062617853953><:moustache:236092022312665089><:ballouminatti:236132317603561475><:1982:236092769779712000><:nope:236096818180653057><:notapproved:236096861113417728><:fedora1:236131582468030474><:happy:236137265305223168><:flowers:236139383764418560><:notbad:236140764416049152><:soundboard:236147928547328000>',

}
messageIndex = {
    # Returns the corresponding text unless it interferes with a command beginning with the PREFIX
    'rickroll': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'xcq': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'it\'s time to stop': 'https://www.youtube.com/watch?v=2k0SmqbBIpQ',
    'stop': 'https://www.youtube.com/watch?v=2k0SmqbBIpQ'
}
containsMessageIndex = {
    # Returns the corresponding text if it contains the keyword unless it interferes with the pMI or mI
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
    'america' : 'America is dead. All hail Rumpland.',
    'rump' : 'FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK https://www.youtube.com/watch?v=AtbMnixO2nc FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK RUMP'
}
# The message to display on the help command (in the on_message async event)
helpMessage = """```
Welcome to VictiBot!
Some sample commands:
    !ping
    !about
    !hello
There are a few more but not all are available on every server
To display this message type !help
```"""
# Combined blacklist/whitelist of users
botCommanders = {
    'Adrian#7972' : True,
    'MoonMoon#9830' : True,
    'Timmy#6089' : True
}
# Add as many insults as you want.
insultList = [
    ', your face reminds me of a nasty little Pumpkin.',
    ', your face causes me distress.',
    ', is your ass jealous of the amount of shit that just came out of your mouth?',
    ', I could eat a bowl of alphabet soup and shit out a smarter statement than that.',
    ', a guy with your IQ should have a low voice too!',
    ', after meeting you, I\'ve decided I am in favor of abortion in cases of incest.',
    ', learn from your parents\' mistakes - use birth control!',
    ', calling you stupid would be an insult to stupid people.',
    ', can I borrow your face for a few days while my ass is on vacation?',
    ', did your parents ever ask you to run away from home?',
    ', ever wondered what your life would be like if you\'d had enough oxygen at birth?',
    ', don\'t feel bad, a lot of people have no talent whatsoever!',
    ', don\'t let your mind wander. It\'s too little to go out alone.',
    ', have you ever felt a feeling of emptyness... In your skull?',
    ', everyone has the right to be ugly, but you have abused the privilege.',
    ', please grasp your ears firmly and remove your head from your ass.',
    ', If you\'re gonna be a smartass, first you have to be smart. Otherwise you\'re just an ass.',
    ', You\'re so ugly, when you popped out the doctor said \"Aww what a treasure\" and your mom said \"Yeah, lets bury it.\"',
    ', Somewhere out there is a tree, tirelessly producing oxygen so you can breathe. I think you owe it an apology.',
    ', You\'re so ugly you scare the shit back into people.',
    ', Why don\'t you slip into something more comfortable -- like a coma.',
    ', You\'re the reason the gene pool needs a lifeguard.',
    ', Why don\'t you check eBay and see if they have a life for sale.',
    ', You didn\'t fall out of the stupid tree. You were dragged through dumbass forest.',
    ', I\'d like to see things from your point of view but I can\'t seem to get my head that far up my ass.',
    ', If laughter is the best medicine, your face must be curing the world.',
    ', I wasn\'t programmed with enough middle fingers to let you know how I feel about you. 凸 (｀0´)凸'
]
insult2List = [
    'Hey ',
    'Yo ',
    'Whattup '
]
#@bot.event
#async def on_ready():
#    print('Logged in as ' + bot.user.name + ' (ID ' + bot.user.id + ').')
#    print('------')
#    # Turns out this is annoying
#    await client.send_message(client.get_channel('228121885630529536'), 'Victibot is online and ready! Currently running as ' + client.user.name + ' (ID ' + client.user.id + ').')

@client.async_event
# Let the user know that the bot is online
def on_ready():
    print('Logged in as ' + client.user.name + ' (ID ' + client.user.id + ').')
    print('------')
    # Turns out this is annoying
    yield from client.send_message(client.get_channel(lastchannel), 'Victibot is online and ready! Currently running as ' + client.user.name + ' (ID ' + client.user.id + '). Last updated by user: ' + lastuser + ' on ' + lasttime + ' (UTC). Enjoy your time with VictiBot as we watch civilization fall to pieces!')

@client.async_event
# Process and respond to all messages the bot receives
def on_message(message):
    """Catch a user's messages and figure out what to return."""
    foundNoCommands = True
    msg = message.content.lower()
    localtime = time.asctime( time.localtime(time.time()) )
    timezone = time.altzone
    msg = message.content
    returnMsg = ''
    # Log non-bot messages
    if not message.author.bot:
        try:
            yield from client.send_message(client.get_channel('243737800992751617'), str(message.author) + ' Said: ' + msg + ' At: ' + localtime + ' (UTC) on channel: ' + message.channel.name + ' of server: ' + message.server.name)
        except:
            pass
    # Only send back message if user that sent the triggering message isn't a bot
    msg = message.content.lower()
    if (not message.author.bot):
        foundNoCommands = False
        # Special returns!
        # About message
        if msg.startswith(PREFIX + 'about'):
            returnMsg = ('VictiBot is a chatbot for Team 1418\'s Discord server. Bot is currently running as ' + client.user.name + ' (ID ' + client.user.id + '). View on GitHub: https://github.com/aderhall/victibot-1')
            returnMsg = returnMsg + '\n' + ('Discuss VictiBot on VictiBot Hub: https://discord.gg/HmMMCzQ')
        # Get xkcd comic
        elif msg.startswith('xkcd'):
            # Store the number/other content after the '!xkcd '.
            comic = msg[5:]

            # If the user included a specific comic number in their message, get the JSON data for that comic. Otherwise, get the JSON data for the most recent comic.
            r = requests.get('http://xkcd.com/' + comic + '/info.0.json' if comic else 'http://xkcd.com/info.0.json')

            # Send the URL of the image from the JSON fetched above.
            # The title text is half of the comic
            returnMsg = (r.json()['img'])
            returnMsg = returnMsg + '\n' + (r.json()['alt'])
        # Get nasa pics
        elif msg.startswith(PREFIX + 'nasa'):
            # Grab JSON data from apod
            r = requests.get('https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY')

            # Send URL for image along with image's title
            returnMsg = (r.json()['url'])
            returnMsg = returnMsg + '\n' + (r.json()['title'])
            returnMsg = returnMsg + '\n' + ('Explanation: ' + r.json()['explanation'])
        # Automatically save session data, update from github, and restart
        elif msg == (PREFIX + 'update'):
            # Confirm that the bot is updating
            returnMsg = ('Updating...')
            localtime = time.asctime( time.localtime(time.time()) )
            timezone = time.altzone
            print ('Time and Date: ' + localtime + ' UTC + (' + str(timezone) + ')')
            # Start a git pull to update bot
            updateresults = (str(subprocess.Popen('git pull', shell=True, stdout=subprocess.PIPE).stdout.read()))
            print (updateresults)
            print ('Username: ' + str(message.author))
            print (str(subprocess.Popen('touch lastchannel && echo "' + str(message.channel.id) + '" | cat > lastchannel && echo "' + str(message.author) + '" cat >> lastchannel', shell=True, stdout=subprocess.PIPE).stdout.read()))
            print (str(subprocess.Popen('touch lasttime && echo "' + localtime + '" | cat > lasttime', shell=True, stdout=subprocess.PIPE).stdout.read()))
            print ('Local Time: ' + localtime)
            returnMsg = returnMsg + '\n' + ('Update Successful! Restarting...')
            # Restart
            subprocess.Popen('python3 bot.py', shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
            os.abort()
        # Mute function still a work in progress, considering deprecating it
        elif msg.startswith(PREFIX + 'mute'):
            name = message.content[6:]
            returnMsg = ('User ' + name)
            member = discord.Server.get_member_named(discord.Server.members, 'GeneralGreat')
            returnMsg = returnMsg + '\n' + ('Member ID' + member)
            discord.add_roles(member, 'muted')
            returnMsg = returnMsg + '\n' + ('Muted ' + name + ' (' + member + ')')
        # Annoy people who post all-caps messages
        elif message.content.isupper() and len(message.content) > 5:
            # if someone sends a message in all caps, respond with a friendly reminder
            returnMsg = ("Did that _really_ need to be in all caps?")
        elif msg.startswith(PREFIX + 'wikihow'):
            returnMsg = ('https://wikihow.com/' + replace(msg[9:], ' ', '-'))
        # Get wikipedia link
        # TODO: get lxml working to display the overview from the page to the output
        elif msg.startswith(PREFIX + 'wiki'):
            returnMsg = ('https://en.wikipedia.org/wiki/' + replace(msg[6:], ' ', '_'))
        # Abuse people
        elif msg.startswith(PREFIX + 'abuse'):
            # Check authorization of the user (necessary to avoid people spamming !abuse @everyone)
            try:
                # Check to see if the user has the True override in the botCommanders object
                botcommand = botCommanders[str(message.author)]
            except:
                # Default for now is no access
                botcommand = False
            # Mainly a debug function but also lets people know that this function has restrictions
            returnMsg = ('Checking authorization for ' + str(message.author))
            # Name default is string to avoid errors for now
            name = ''
            # Only abuse if a member is mentioned, will incorporate a for loop for recursive abuse
            if len(message.mentions) > 0:
                # Try to get the mention string
                try:
                    name = msg[7:]
                    print ('Name: ' + name)
                    # These are now obsolete but I may use them in the future
                    #name = message.server.get_member_named(name)
                    print ('Name: ' + str(name))
                    #name = str(name.mention)
                    print ('Name: ' + name)
                except:
                    # Default to notice if user cannot be found, resorts to abusing everyone
                    returnMsg = ('Could not find user: ' + name)
                    print ('Found exception')
                    name = '@everyone'
                # Only send further messages if user is authorized
                if botcommand:
                    # Attempt to print the nick of a member containing the username (for debug purposes)
                    try:
                        print ('User Nick: ' + message.server.get_member_named(msg[7:]).nick)
                    except:
                        pass
                    #Abuses the member specified (First line for debugging only)
                    #returnMsg = ('Abusing ' + name + '.')
                    returnMsg = returnMsg + '\n' + (random.choice(insult2List) + '' + name + '' + random.choice(insultList))
                else:
                    # Let the user know that the authorization failed
                    returnMsg = returnMsg + '\n' + ('You are not authorized to use the abuse command.')
        # Help message
        elif msg.startswith('!help'):
            returnMsg = ('A list of basic commands has been sent to you via DM')
            yield from client.send_message(message.author, helpMessage)
        # Generate an invite link for adding VictiBot to a server
        elif  msg.startswith(PREFIX + 'invite'):
            returnMsg = ('An invite code to add VictiBot to a server you manage has been sent to you via DM')
            yield from client.send_message(message.author, 'Add ViciBot to a server using this link: ')
            yield from client.send_message(message.author, 'https://discordapp.com/oauth2/authorize?client_id=231595610682294272&scope=bot&permissions=0')
            yield from client.send_message(message.author, 'Note: You can only add VictiBot to a server if you have the \'Manage server\' privilege on it.')
        # List all servers that the bot can see
        elif msg.startswith(PREFIX + 'servers'):
            # Accumulation text variable
            actext = ''
            # Recursively get name of each server
            for i in client.servers:
                actext = actext + i.name + ', '
            # Display a list of all servers (slicing to remove  final comma space)
            returnMsg = (actext[:-2])
        # Same as above but with channels
        elif msg.startswith(PREFIX + 'channels'):
            actext = ''
            for i in client.get_all_channels():
                actext = actext + i.name + ', '
            returnMsg = (actext[:-2])
        # Same as above but with member nicknames
        elif msg.startswith(PREFIX + 'members'):
            actext = ''
            for i in client.get_all_members():
                try:
                    # Gets nick instead of name (nick is member nickname as string)
                    actext = actext + i.nick + ', '
                except:
                    pass
            returnMsg = (actext[:-2])
        # Spams repeatedly up to ten times (restricted function)
        elif msg.startswith(PREFIX + 'spam'):
            # Check authorization for use of this function
            try:
                botcommand = botCommanders[str(message.author)]
            except:
                # Default to blacklisting
                botcommand = false
            returnMsg = ('Checking authorization for ' + str(message.author))
            # Do the actions only if authorization succeeded
            if botcommand:
                # Attempt to get the specified number of spam messages to send
                if len(msg) > 6:
                    try:
                        times = int(msg[6:])
                    except:
                        # Should only be called if the user inputs a non-integer value for the number of spam messages
                        # Defaults to 5 messages
                        times = 5
                # Recursion index starting at one to avoid user confusion (should probably fix this at some point)
                count = 1
                # Limit to 10 times
                while (count <= times) and (count < 11):
                    # The spam message (potential monty python reference could go here)
                    returnMsg = returnMsg + ('\nSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpamSpam')
                    # Wait without blocking the async event loop
                    asyncio.sleep(0.5)
                    # Standard incrementation of count
                    count += 1
            else:
                # Let the user know that the authorization failed
                returnMsg = ('You are not authorized to use this function')
        # Respond to messages from dictionaries (to make code more efficient)
        else:
            foundNoCommands = True
            print ('Found no commands!')
            # Respond if the message has a basic, static response.
            # Attempt to retrieve response from a dictionary
            # Note: I know very well that this is not the most efficient way to respond to commands
            # It is not very async-style and it ends up doing quite a lot at a very high level even when messages with no command are given
            # However, certain features, such as the log and the more general contains() response are much simpler in this structure
            # I do not plan to change this at the moment
            # TODO: Add a new dictionary for commands to respond to messages containing the keyword
            try:
                # Prefix commands take priority over standard text commands
                returnMsg = (prefixMessageIndex[(msg)])
                # Debugging purposes only
                #print ('Prefix Done')
            except:
                try:
                    returnMsg = (messageIndex[msg])
                except:
                    for key, value in containsMessageIndex.items():
                        if contains(msg, key) >= 1:
                            returnMsg = (value)
    if (not message.server.name == 'Team 1418') and (not foundNoCommands):
        yield from client.send_message(message.channel, returnMsg)

@client.async_event
# Respond on a new member joining
def on_member_join(member):
    yield from client.send_message(member.server.default_channel, '**Welcome ' + member.mention + ' to the ' + member.server.name + ' server!**')

# Respond on member leaving
@client.async_event
def on_member_remove(member):
    yield from client.send_message(member.server.default_channel, member.name + ' left the server :frowning: RIP ' + member.name)


# Get token from token.txt
with open('token.txt', 'r') as token_file:
    # Parse into a string, and get rid of trailing newlines
    token = token_file.read().replace('\n', '')
# It is only fair that whoever is running the bot should know their own token
print('Starting with token ' + token + '...')

# Start bot!
client.run(token)

# That's all, folks.
