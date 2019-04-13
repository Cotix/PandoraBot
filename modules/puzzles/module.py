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
        if(results):
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

    @command
    def coordinates(self, numbers):
        """
        Geeft alle mogelijke locaties op de campus met coordinaten bestaande uit de gegeven getallen. Getallen dienen te worden gescheiden met komma's
        """
        number_list = numbers.split(',')

        if all([x.isdigit() for x in number_list]):
            results = util.brute_force_coordinates(number_list)
            self.respond('Er zijn %i locaties op de campus met deze getallen.' % (len(results)))
            if(results):
                if len(results) <= 5:
                    for result in results:
                        self.send_location(result[0], result[1])
                elif len(results) <= 15:
                    self.respond('\n'.join(['%s, %s' % x for x in results]))
        else:
            self.respond('Verkeerde input. Ik verwacht bijvoorbeeld \'/coordinates 52,248,219,6,85,40,38\'.')

    def send_location(self, lat, lon):
        self.bot.sendLocation(self.update.message.chat_id, latitude=lat, longitude=lon)

    @command
    def ascii(self, numbers):
        """
        Vertaalt de waarden naar ASCII-tekens. ASCII-waarden van letters liggen tussen de 65 en de 121. De inputwaarden dienen gescheiden te worden met komma's.
        """
        number_list = numbers.split(',')
        if all([x.isdigit() for x in number_list]):
            result = util.numbers_to_ascii_characters(number_list)
            self.respond(numbers + ': ' + result)
        else:
            self.respond('Verkeerde input. Ik verwacht bijvoorbeeld \'/ascii 84,101,115,116\'.')

    @command
    def base(self, numbers, base_x, base_y):
        """
        Converteert de waarden van de ene base naar de andere base. Er kunnen meerdere waarden tegelijk omgezet worden door deze te scheiden met komma's.
        """
        try:
            base_x = int(base_x)
            base_y = int(base_y)
        except ValueError:
            self.respond('Verkeerde input. Bases moeten getallen zijn.')
            return
        if base_x < 2 or base_y < 2 or base_x > 36 or base_y > 36:
            self.respond('Verkeerde input. Bases moeten tussen de 2 en de 36 liggen.')
            return

        number_list = numbers.split(',')
        if all([util.is_in_base(x, base_x) for x in number_list]):
            self.respond('\n'.join([number + ' wordt ' + util.base_x_to_base_y(number, base_x, base_y) for number in number_list]))
        else:
            self.respond('Verkeerde input. De waarden komen niet overeen met de base.')
