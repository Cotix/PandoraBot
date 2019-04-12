# PandoraBot
Install dependencies using `pipenv install`. Then simply run `pipenv run python main.py`, or `pipenv shell` to start an interactive shell in the environment.

Make sure to set the TOKEN environment variable to your telegram API token.

### Telegram framework
This telegram bot relies on [the python-telegram-bot library.](https://python-telegram-bot.readthedocs.io/en/stable/)

However, this library does not offer as much abstraction and structure as I would like. As such we make use of a self-written layer above the telegram framework. Most of this can be found in the `modules/telegram_module.py` classes. This abstraction layer allows programmers to automate/not deal with all the registering of callbacks, parsing commands, checking for errors etc.

Instead we define 'modules' in the modules package. Every module is responsible for a certain type of functionality. For example, the iapandora module is responsible for communicating with the iapandora.nl website, and the puzzles module offers some utility functions to solve puzzles.
Every module should have a module.py, in which a `TelegramModule` class is defined. This class can implement telegram commands and filters.

A quick example:
```
from modules.telegram_module import TelegramModule
from modules.telegram_module import command


class ExampleModule(TelegramModule):

    @command
    def concat(self, first_argument, second_argument):
        """
        This function takes two arguments, and returns the
        concatination of the two arguments
        """
        self.respond(f'{first_argument} {second_argument}')
 ```
 
 This is a very simple example of a basic `/concat <arg1> <arg2>` command within an ExampleModule. The arguments defined as function parameters will be parsed by the abstraction layer. When an incorrect amount of arguments is supplied by the user, an error message will be sent back containing the proper usage of the function and the help text defined as doc in the function(seen in the example). This doc is also used in the help module, to supply every command with a description
 
 #### Different functions
 In the example above the `@command` annotation was showcased. This is the most obvious and basic function a TelegramModule can define. The possible annotation (as of now) include:
 
 - command
 - photo
 - location
 
 Photo and location will be called when a user shares a photo or a location, respectively. Usage is very similar, and examples can be found in the codebase.
 
 
 #### TelegramModule instance variables and functions
 For every request that is made, a new instance of your module will be created. These instances will have a few variables and functions available that help with developing new modules.
 
 Instance variables available:
 
 - self.bot
    
    The bot argument inherited from the python-telegram-bot library. This can be used to send complex messages like locations or photos.
 - self.update
 
     Inherited from the python-telegram-bot aswel. This contains all information about the corresponding message that triggered this function. This includes things like chat, message or user ids, full body text, timestamp, attachments, etc.
 - self.context
 
    Dict that is unique to the user that triggered the function. This dict is persistent over multiple requests and can be used to store variables like auth or location data, that might be used in a different function (in a different module).
 
 

 Instance functions are:
 
 -  self.respond(msg):
 
    Responds to the message that triggered the function. This only supports text messages.
 
 -  self.ask_options(options, question='Wat bedoel je?', n_cols=3, default=None,
                   values=None, timeout=settings.KEYBOARD_TIMEOUT)
    
    Asks the user a question using a custom inline keyboard that dissapears after first use. An example will be given below, as this is very useful in designing user friendly functions.
    This function will block until the user responded or the timeout has been reached, in which case the default value is returned.
    
#### More module examples


##### Asking for options
One of the more advanced features is presenting custom options to the user.

```
from modules.telegram_module import TelegramModule
from modules.telegram_module import command


class OptionExamples(TelegramModule):

    @command
    def concat(self, first_argument, second_argument):
        """
        This function takes two arguments, and returns the
        concatination of the two in any order the user desires
        """
        if self.ask_option(['A+B', 'B+A']) == 'B+A':
            self.respond(f'{second_argument} {first_argument}')
        else:
            self.respond(f'{first_argument} {second_argument}')
```



##### Receiving and sending locations
```
import datetime

from modules.telegram_module import TelegramModule, location, command

LOCATIONS = dict()


class Location(TelegramModule):
    @location
    def recv_location(self):
        print(self.update)
        if hasattr(self.update, 'edited_message') and self.update.edited_message:
            msg = self.update.edited_message
        else:
            msg = self.update.message
        loc = msg['location']
        self.context['location'] = {'longitude': loc.longitude, 'latitude': loc.latitude}
        self.context['location']['date'] = msg['edit_date'] or msg['date']
        LOCATIONS[msg['chat']['first_name'].lower()] = self.context['location']

    @command
    def where(self, firstname):
        """
        Geeft de locatie van een teamgenoot terug.(Mits deze live locatie aan heeft staan)
        """
        firstname = firstname.lower()
        if firstname in LOCATIONS:
            loc = LOCATIONS[firstname]
            self.bot.sendLocation(self.update.message.chat_id, latitude=loc['latitude'],
                                  longitude=loc['longitude'])
            self.respond('Deze locatie update is %i minuten oud.' %
                         ((datetime.datetime.now() - loc['date']).seconds//60))
        else:
            self.respond('%s heeft helaas zijn locatie delen niet aanstaan!' % firstname)

```

