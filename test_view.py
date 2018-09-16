''' Test file '''
import unittest
from unittest.mock import Mock

import time

from telepot.namedtuple import ReplyKeyboardMarkup

from view import View

class TestUM(unittest.TestCase):
    ''' class TestUM '''

    markup = ReplyKeyboardMarkup(keyboard=[['Start', 'Circle'], ['Stop']])
    msg = {'message_id': 4076,
           'from':
               {
                   'id': 563019151, 'is_bot': False,
                   'first_name': 'Ludmila', 'language_code': 'ru-ru'
               },
           'chat':
               {
                   'id': 563019151, 'first_name': 'Ludmila',
                   'type': 'private'
               },
           'date': 1535890978, 'text': 'Stop'}
    chat_id = '563019151'
    first_name = 'Ludmila'
    text_stop = 'Stop'
    text_start = 'Start'
    text_circle = 'Circle'
    date = '1535890978'
    start = 0
    stop = 0
    bot = Mock()
    db_runner = Mock()
    logger = Mock()
    view_test = View(bot=bot, db_runner=db_runner, logger=logger)

    def test_view_unresolved_choice(self):
        ''' testing view_unresolved_choice '''
        self.view_test.unresolved_choice(self.msg)
        self.bot.sendMessage.assert_called_with(int(self.chat_id), self.first_name +
                                                ', please choose button Start or Stop',
                                                reply_markup=self.markup)

    def test_view_text_start(self):
        ''' testing view_text_start '''
        self.view_test.start = 1
        self.view_test.text_start(self.date, int(self.chat_id), self.first_name)
        self.db_runner.insert_runner.assert_called_with(int(self.chat_id),
                                                        self.first_name, self.date,
                                                        (''.join(str(self.chat_id) + '_' +
                                                                 str(self.view_test.start))))

    def test_view_text_circle(self):
        ''' testing view_text_circle '''
        self.view_test.start = 1
        self.view_test.text_circle(self.date, int(self.chat_id), self.first_name)
        self.db_runner.insert_runner.assert_called_with(int(self.chat_id),
                                                        self.first_name, self.date,
                                                        (''.join(str(self.chat_id) + '_' +
                                                                 str(self.view_test.start))))

    def test_view_text_stop(self):
        ''' testing view_text_stop '''
        self.view_test.start = 1
        self.view_test.text_stop(self.date, self.first_name, int(self.chat_id))
        self.db_runner.insert_runner.assert_called_with(int(self.chat_id),
                                                        self.first_name, self.date,
                                                        (''.join(str(self.chat_id) + '_' +
                                                                 str(self.view_test.start))))

    def test_view_date_format(self):
        ''' testing view_date_format '''
        assert time.strftime('%H:%M:%S', time.gmtime(int(self.date)))

    def test_view_test_type(self):
        ''' testing view_test_type '''
        assert self.msg.get('text')

    def test_view_circle_time(self):
        ''' testing view_circle_time '''
        self.view_test.start = 1
        assert self.db_runner.select_circles(''.join(str(self.chat_id) + '_' +
                                                     str(self.view_test.start)))

    def test_view_calculate_run_time(self):
        ''' testing view_calculate_run_time '''
        self.view_test.start = 1
        self.view_test.run_time_db = 2
        assert self.db_runner.run_time(''.join(str(self.chat_id)+'_'+
                                               str(self.view_test.start)))
        assert self.db_runner.best_run_time(self.chat_id)
        assert self.db_runner.circle_count(''.join(str(self.chat_id)+'_'+
                                                   str(self.view_test.start)))
