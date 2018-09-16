''' Project telegramm bot for runners '''
import time
import logging
from telepot.namedtuple import ReplyKeyboardMarkup


class View:
    ''' main class View '''
    start = 0
    stop = 0
    markup = ReplyKeyboardMarkup(keyboard=[['Start', 'Circle'], ['Stop']])
    module_logger = logging.getLogger("telegramm_bot.view")

    def __init__(self, bot, db_runner, logger):
        '''        initialization View        '''
        self.bot = bot
        self.db_runner = db_runner
        self.logger = logger

    def nul_values(self):
        '''        set null values        '''
        self.start = 0
        self.stop = 0

    def unresolved_choice(self, msg):
        '''       massage if user didn't enter text       '''
        self.bot.sendMessage(msg['chat']['id'], msg['chat']['first_name'] +
                             ', please choose button Start or Stop',
                             reply_markup=self.markup)
        logger = logging.getLogger('telegramm_bot.view.unresolved_choice')
        logger.warning(f"user didn't enter text, "
                       f"chat_id: %s, "
                       f"first_name: %s | log method: %s",
                       msg['chat']['id'], msg['chat']['first_name'], 'logging with f-string')

    def text_start(self, date, chat_id, first_name):
        '''        if user wrote 'Start'        '''
        self.start = date
        self.db_runner.insert_runner(chat_id, first_name, date,
                                     (''.join(str(chat_id) + '_' + str(self.start))))
        logger = logging.getLogger('telegramm_bot.view.text_start')
        logger.info(f'user entered "Start", chat_id: %s, '
                    f'first_name: %s | log method: %s',
                    chat_id, first_name, 'logging with f-string')

    def text_circle(self, date, chat_id, first_name):
        '''        if user wrote 'Circle'        '''
        logger = logging.getLogger('telegramm_bot.view.text_circle')
        logger.info('user entered "Circle", chat_id: %s, '
                    f'first_name: %s | log method: %s',
                    chat_id, first_name, 'logging with f-string')
        self.db_runner.insert_runner(chat_id, first_name, date,
                                     (''.join(str(chat_id) + '_' + str(self.start))))

    def text_stop(self, date, first_name, chat_id):
        '''        if user wrote 'Stop'        '''
        logger = logging.getLogger('telegramm_bot.view.text_stop')
        logger.info('user entered "Stop", chat_id: %s, '
                    f'first_name: %s | log method: %s',
                    chat_id, first_name, 'logging with f-string')
        self.stop = date
        self.db_runner.insert_runner(chat_id, first_name, date,
                                     (''.join(str(chat_id)+'_'+str(self.start))))

    @staticmethod
    def date_format(date):
        '''        verification date format        '''
        logger = logging.getLogger('telegramm_bot.view.date_format')
        try:
            new_date = time.strftime('%H:%M:%S', time.gmtime(date))
            return new_date
        except TypeError as error:
            logger.warning('TypeError date: %(date)')
            return error

    def circle_time(self, chat_id, first_name):
        '''        calculate circle time        '''
        logger = logging.getLogger('telegramm_bot.view.circle_time')
        c_runner = self.db_runner.select_circles(''.join(str(chat_id) + '_' + str(self.start)))
        for ind, value in sorted(enumerate(c_runner[1:])):
            self.bot.sendMessage(chat_id, f'{ind+1} circle: '
                                          f'{View.date_format(value - c_runner[ind])}')
        logger.info('calculate circle time, chat_id: %s, '
                    f'first_name: %s | log method: %s',
                    chat_id, first_name, 'logging with f-string')

    def calculate_run_time(self, chat_id, first_name):
        '''        calculate run time        '''
        logger = logging.getLogger('telegramm_bot.view.calculate_run_time')
        run_time_db = self.db_runner.run_time(''.join(str(chat_id)+'_'+str(self.start)))
        best_run_time_db = self.db_runner.best_run_time(chat_id)
        circle_count_db = self.db_runner.circle_count(''.join(str(chat_id)+'_'+str(self.start)))
        self.bot.sendMessage(chat_id, f'Run time is: {run_time_db}',
                             reply_markup=self.markup)
        if best_run_time_db == run_time_db:
            self.bot.sendMessage(chat_id, 'The best time! Congrats!!!')
        else:
            self.bot.sendMessage(chat_id, f'The best run time is: {best_run_time_db}')

        self.bot.sendMessage(chat_id, f'Count of circles: {circle_count_db}')
        logger.info('calculate run time, chat_id: %s, '
                    f'first_name: %s | log method: %s',
                    chat_id, first_name, 'logging with f-string')
        View.nul_values(self)
        logger.info('set null values, chat_id: %s, '
                    f'first_name: %s | log method: %s',
                    chat_id, first_name, 'logging with f-string')

    def test_type(self, msg):
        '''        testing types of massages.        '''
        logger = logging.getLogger('telegramm_bot.view.test_type')
        logger.info("testing types of massages, chat_id: %s, "
                    f"first_name: %s | log method: %s",
                    msg['chat']['id'], msg['chat']['first_name'],
                    'logging with f-string')
        try:
            msg.get('text')
            return None
        except KeyError as error:
            logger.warning("user did not enter text: KeyError, "
                           "chat_id: %s, first_name: %s | log method: %s",
                           msg['chat']['id'], msg['chat']['first_name'],
                           'logging with f-string')
            self.bot.sendMessage(msg['chat']['id'], 'Choose the button')
            return error

    def root_handle(self, msg):
        '''        main function.        '''
        print(msg)
        logger = logging.getLogger('telegramm_bot.view.root_handle')
        View.test_type(self, msg)
        if msg['text'] == "Start":
            View.text_start(self, msg['date'], msg['chat']['id'],
                            msg['chat']['first_name'])
        elif msg['text'] == "Circle":
            if self.start > 0:
                View.text_circle(self, msg['date'], msg['chat']['id'], msg['chat']['first_name'])
            else:
                self.bot.sendMessage(msg['chat']['id'], f"first press the \'Start\' button",
                                     reply_markup=self.markup)
                logger.warning("User pressed 'Circle', 'Start' was not pressed, "
                               "chat_id: %s, first_name: %s | log method: %s",
                               msg['chat']['id'], msg['chat']['first_name'],
                               'logging with f-string')
        elif msg['text'] == "Stop":
            if self.start > 0:
                View.text_stop(self, msg['date'], msg['chat']['first_name'], msg['chat']['id'])
                View.circle_time(self, msg['chat']['id'], msg['chat']['first_name'])
                View.calculate_run_time(self, msg['chat']['id'], msg['chat']['first_name'])
            else:
                self.bot.sendMessage(msg['chat']['id'], f"first press the \'Start\' button",
                                     reply_markup=self.markup)
                logger.warning("User pressed 'Stop', 'Start' was not pressed, "
                               "chat_id: %s, first_name: %s | log method: %s",
                               msg['chat']['id'], msg['chat']['first_name'],
                               'logging with f-string')
        else:
            View.unresolved_choice(self, msg)
