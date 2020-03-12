# meowBot >.< - a simple discord bot

Hello! Welcome to ***meowBot***! :3

This project mainly originated from me seeking a new programming experience other than C++ - Python. 
With this, I could step into the fundamentals of Python and learn a new library / framework used to create Discord bots.
This simple framework is known as ***discord.py***, and with it comes many functions that Discord users use on a daily basis!
Hence, my inspiration to create my own discord bot came with consistently using Discord as a platform to communicate
with friends and family. 

Below can be seen a general outline of the things that meowBot can accomplish!

# ***General Commands***
Some useful commands to access meowBot:

```m.help``` - Lists the commands currently available for the user.

```m.musichelp``` - Lists the commands to access music functions.

```m.misc``` - Lists fun and miscellaneous functions.

```m.intro``` - Greets the user.

```m.users``` - Prints number of users.

```m.purge (num)``` - Purges however many messages you provide it prior to sending command.

# ***Music Commands***
Some useful commands to access meowBot's music functionality:

```m.join``` - Adds the bot to a voice channel if user is already in one. Otherwise, nothing will happen.

```m.leave``` - Takes meowBot out of whatever channel the user is in.

```m.play (url) | m.play search term``` - Plays youtube url given to the bot from the user.

```m.pause``` - Pauses the current song playing.

```m.resume``` - Resumes the current song on queue.

```m.stop``` - Completely stops song in order to pass a new url to the bot.

# ***Miscellaneous Commands***
Some fun and miscellaneous functions that meowBot offers:

```m.quote``` - Prints a random quote for you fellas feeling under the weather.

```m.dadprogjoke``` - Provides the user with a funny dad programming joke, if you're into that stuff.

```m.jojo``` - Plays the infamous Giorno's Theme from Jojo's Bizarre Adventure. Pretty cool, I know.

# **Behind The Scenes**
Things that meowBot could possibly perform in the background include:

```on_message_delete``` - Sends a warning message in a logs channel notifying moderators who deleted a message.

```on_member_join``` - Greets the user upon joining the server, and assigns the member with an introductory role.