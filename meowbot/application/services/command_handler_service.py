from discord.ext import commands
from meowbot.utils import logging, setup_logger

class CommandHandlerService:
    def __init__(self):
        self.logger = setup_logger(name="service.command.handler", level=logging.INFO)
        self.commands_tally = {}
    
    # TODO: can be improved by metric firing on command usage
    def serve_on_command_event(self, ctx):
        if ctx.command is not None:
            if ctx.command.name in self.commands_tally:
                self.commands_tally[ctx.command.name] += 1
            else:
                self.commands_tally[ctx.command.name] = 1
        self.logger.info(f"{ctx.command.name} was served.")
    