from config.telegram import updater
import modules
import modules.telegram_module

modules.telegram_module.init()
updater.start_polling()
