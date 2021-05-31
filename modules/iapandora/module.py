from modules.iapandora.iapandora_client import IAPandoraClient
from modules.telegram_module import TelegramModule
from modules.telegram_module import command


class IAPandora(TelegramModule):

    @command
    def auth(self, username, password):
        """
        Dit commando kopelt iapandora.nl login gegevens aan jouw account.
        Hierdoor kun je gebruik maken van extra functionaliteit zoals het automatisch
        inleveren van killcodes en puzzels.
        """
        client = IAPandoraClient()
        if client.login(username, password):
            self.context['username'] = username
            self.context['password'] = password
            self.context['client'] = client
            self.respond('Succesvol ingelogd! Je kan nu alle iapandora.nl '
                         'functionaliteit gebruiken')
        else:
            self.respond('Het is niet gelukt om in te loggen. Heb je wel de goeie '
                         'inloggegevens gegeven?')

    @command
    def auth_david(self, password):
        self.auth("haha trek ad", password)

    @command
    def kill(self, code):
        """
        Dit command vult een killcode in op jouw naam.
        """
        if not self.context['client']:
            self.respond('Je moet je eerst authenticeren met /auth!')
        else:
            res = self.context['client'].kill(code)
            if not res:
                self.respond('Het is niet gelukt deze killcode in te vullen :(')
            else:
                self.respond('Killcode is ingevuld! Lekker bezig %s' %
                             self.context['username'])

    @command
    def puzzle(self, code):
        """
        Dit command vult een puzzlecode in.
        """
        if not self.context['client']:
            self.respond('Je moet je eerst authenticeren met /auth!')
        else:
            res = self.context['client'].puzzle(code)
            if not res:
                self.respond('Het is niet gelukt deze puzzle in te vullen :(')
            else:
                self.respond('Puzzle is ingevuld! Lekker bezig %s' %
                             self.context['username'])
