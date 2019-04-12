import inspect
import logging

from telegram.ext import CommandHandler, MessageHandler, Filters
from config.telegram import dispatcher


def command(func):
    func.is_command = True
    return func


def photo(func):
    func.filter = Filters.photo
    return func


def location(func):
    func.filter = Filters.location
    return func


class TelegramModuleMeta(type):
    def __new__(cls, name, bases, dct):
        x = super().__new__(cls, name, bases, dct)
        for name in list(x.__dict__):
            method = getattr(x, name)
            if hasattr(method, "is_command"):
                def get_wrapper(func):
                    complete_arg_spec = inspect.getfullargspec(method)
                    argspec = complete_arg_spec.args
                    has_vararg = inspect.getfullargspec(method).varargs

                    if (argspec[0] != 'self'):
                        raise ValueError('First argument of TelegramCommand should be '
                                         'self')
                    argspec = argspec[1:]

                    def wrapper(bot, update, user_data=None, args=[]):
                        amount_of_method_arguments = len(argspec)
                        amount_of_given_arguments = len(args)
                        not_enough_given_arguments = amount_of_given_arguments < amount_of_method_arguments
                        too_many_given_arguments = amount_of_given_arguments > amount_of_method_arguments

                        ins = x(context=user_data, update=update, bot=bot)
                        if (not_enough_given_arguments) or (too_many_given_arguments and not has_vararg):
                            logging.debug('Command called with invalid argument count')
                            bot.send_message(chat_id=update.message.chat_id,
                                             text='Ongeldig aantal argumenten.')
                            bot.send_message(chat_id=update.message.chat_id,
                                             text=cls.get_help_text(func))
                        else:
                            func(ins, *args)
                    wrapper.original = func
                    return wrapper

                setattr(x, name, get_wrapper(method))

                handler = CommandHandler(name, getattr(x, name), pass_user_data=True,
                                         pass_args=True)
                dispatcher.add_handler(handler)
            elif hasattr(method, 'filter'):
                def get_wrapper(func):
                    def wrapper(bot, update, user_data=None):
                        ins = x(context=user_data, update=update, bot=bot)
                        func(ins)
                    wrapper.original = func
                    return wrapper
                setattr(x, name, get_wrapper(method))
                handler = MessageHandler(method.filter, getattr(x, name),
                                         pass_user_data=True, edited_updates=True)
                dispatcher.add_handler(handler)

        return x

    @staticmethod
    def get_help_text(func):
        fullargspec = inspect.getfullargspec(func)
        argspec = fullargspec.args[1:]
        varargs = fullargspec.varargs

        funcspec = TelegramModuleMeta._build_funcspec(func, argspec)
        varspec = TelegramModuleMeta._build_varspec(varargs)
        helptext = TelegramModuleMeta._build_helptext(func.__doc__ or '')

        return "{func} {varargs}\n{help}".format(func=funcspec,
                                                 varargs=varspec,
                                                 help=helptext)

    @staticmethod
    def _build_funcspec(func, argspec):
        params = ' '.join(['<{arg}>'.format(arg=arg) for arg in argspec])
        return '/{method} {params}'.format(method=func.__name__, params=params)

    @staticmethod
    def _build_varspec(varargs):
        varargstring = ''
        if varargs:
            varargstring = '<*{vararg}>'.format(vararg=varargs)
        return varargstring

    @staticmethod
    def _build_helptext(doc):
        doc = doc.replace('\n', ' ').replace('\t', ' ')
        return ' '.join([x for x in doc.split() if x != ''])


class TelegramModule(metaclass=TelegramModuleMeta):

    def __init__(self, context=None, bot=None, update=None):
        super(TelegramModule, self).__init__()
        self.context = context
        self.bot = bot
        self.update = update

    def respond(self, msg):
        self.bot.send_message(chat_id=self.update.message.chat_id,
                              text=msg)
        logging.log(logging.INFO, 'Sending message: %s' % msg)

