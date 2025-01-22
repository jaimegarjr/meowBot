# meowBot >.< - a simple discord bot

Hello! Welcome to ***meowBot***! :3

Below can be seen a general outline of the things that meowBot can accomplish!
Some of this is also for my future reference in case I ever want to actively work on this project again.

## **Installation**

To install and actually run meowBot on your local machine, perform the following steps.
1. Clone the repo to your local machine - store it in a Projects folder preferably.
2. meowBot uses Poetry for dependency management. To install Poetry, run ```pip install poetry``` in your terminal.
3. Once Poetry is installed, navigate to the directory where the repo is stored and run ```poetry install``` to install all dependencies.
4. From here, create a ```.env``` file that contains the following fields. 
```
BOT_TOKEN = "your_bot_token"
CLIENT_ID = "your_client_id"
```
You may also need to write a `prefixes.json` file that contains a guild ID to prefix mapping. 
```
{
    "guild_id": "prefix"
}
```
5. To run the bot, execute ```poetry run python -m meowbot.bot.meowbot``` in your terminal.


## ***General Commands***
Some useful commands to access meowBot:

```m.help (none, music, misc, channels)``` - Lists commands pertaining to a particular topic.

```m.intro``` - Greets the user.

```m.users``` - Prints number of users.

```m.purge (num)``` - Purges however many messages you provide it prior to sending command.

```m.invite``` - Provides the user with a link to invite meowBot to different servers!

## ***Music Commands***
Some useful commands to access meowBot's music functionality:

```m.join``` - Adds the bot to a voice channel if user is already in one. Otherwise, nothing will happen.

```m.leave``` - Takes meowBot out of whatever channel the user is in.

```m.play (url) | m.play search term``` - Plays a song from youtube given by the user.

```m.pause``` - Pauses the current song playing.

```m.resume``` - Resumes the current song on queue.

```m.stop``` - Completely stops any audio from playing on meowBot.

## ***Channel Commands***
Some useful commands to create and delete channels with meowBot:

```m.create (name)``` - Creates a basic text channel with the given name.

```m.create voice (name)``` - Creates a basic voice channel with the given name.

```m.create priv (name)``` - Creates a private text channel with the given name.

```m.create priv_voice (name)``` - Creates a private voice channel with the given name.

```m.delete (name)``` - Deletes a voice / text channel with the given name.

## ***Miscellaneous Commands***
Some fun and miscellaneous functions that meowBot offers:

```m.quote``` - Prints a random quote for you fellas feeling under the weather.

```m.github``` - Gives the caller a link to the GitHub repo that meowBot runs off of.

```m.dadprogjoke``` - Provides the user with a funny dad programming joke, if you're into that stuff.

```m.profile {other users)``` - Sends the user a detailed tag of their profile on Discord.

## ***Developer Commands***
Listed below are some commands created in order to ease workflow as I developed meowBot:

```m.load (cog file name)``` - Loads a specified cog back into the bot after edits are finished.

```m.reload (cog file name)``` - Reloads a specified cog into the bot during runtime.

```m.unload (cog file name)``` - Unloads a specified cog off the bot in order to allow for edits.