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
5. To run the bot, execute ```poetry run python -m meowbot.bot.meowbot``` in your terminal.
    - You can also make use of the WIP Justfile to run common commands for you.

## **More to come!**