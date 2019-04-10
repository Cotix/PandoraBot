from modules.telegram_module import TelegramModule
from modules.telegram_module import command
from . import util


class Puzzles(TelegramModule):

    @command
    def building(self, number):
        """
        Geeft de gebouwnaam bij een gebouwnummer.
        """
        building = util.building_by_number(number)

        if not building:
            self.respond('Dat gebouwnummer bestaat niet!')

        self.respond('Gebouwnummer %s komt overeen met gebouw %s.' % (number, building.name))

    @command
    def locations(self, length):
        """
        Geeft een lijst met alle locaties die een specifieke lengte hebben
        """
        results = util.location_by_length(length)
        self.respond('Er zijn %i resultaten met lengte %s' % (len(results), length))
        self.respond(', '.join([x.name for x in results]))

    @command
    def locations_with(self, symbols):
        """
        Geeft een lijst met alle locaties waarvan de naam alle gegeven symbolen bevat
        """
        results = util.locations_containing_symbols(symbols)
        self.respond('Er zijn %i resultaten die de symbolen \'%s\' bevatten' % (len(results), symbols))
        self.respond(', '.join([x.name for x in results]))

    @command
    def buildings(self, length):
        """
        Geeft een lijst met alle gebouwen die een specifieke lengte hebben
        """
        results = util.buildings_by_length(length)
        self.respond('Er zijn %i gebouwen met lengte %s' % (len(results), length))
        self.respond(', '.join([str(x) for x in results]))

    @command
    def buildings_with(self, symbols):
        """
        Geeft een lijst met alle gebouwen waarvan de naam alle gegeven symbolen bevat
        """
        results = util.buildings_containing_symbols(symbols)
        self.respond('Er zijn %i gebouwen die de symbolen \'%s\' bevatten' % (len(results), symbols))
        self.respond(', '.join([str(x) for x in results]))
