''' DB logic file '''
import sqlite3
import logging

class DbRunner:
    ''' class DB '''
    db = 'db_runner.sqlite'
    def __init__(self):
        logger = logging.getLogger('telegramm_bot.view.db_runner_init')
        try:
            conn = sqlite3.connect(self.db)
            c_db_runner_init = conn.cursor()
            c_db_runner_init.execute('''DROP TABLE if exists runner''')
            c_db_runner_init.execute('''CREATE TABLE if not exists runner(
            chat_id INTEGER,
            first_name VARCHAR(40),
            circle_time INTEGER,
            circles_id VARCHAR(150)
            )''')
            conn.commit()
            c_db_runner_init.close()
            logger.warning("connect with DB is ok")
        except ConnectionError:
            logger.warning("connect with DB is fale")

    def insert_runner(self, chat_id, first_name, circle_time, circles_id):
        ''' insert data to DB '''
        logger = logging.getLogger('telegramm_bot.view.insert_runner')
        try:
            conn = sqlite3.connect(self.db)
            c_insert_runner = conn.cursor()
            params = (chat_id, first_name, circle_time, circles_id)
            c_insert_runner.execute('''
            INSERT INTO runner (chat_id, first_name, circle_time, circles_id)
             VALUES(?, ?, ?, ?)
            ''', params)
            logger.info(f'insert_runner is ok, chat_id: %s, '
                        f'first_name: %s | log method: %s',
                        chat_id, first_name, 'logging with f-string')
            conn.commit()
            c_insert_runner.close()
        except AttributeError:
            logger.info(f'insert_runner is fale, chat_id: %s, '
                        f'first_name: %s | log method: %s',
                        chat_id, first_name, 'logging with f-string')

    def run_time(self, circles_id):
        ''' calculate run time'''
        conn = sqlite3.connect(self.db)
        c_run_time = conn.cursor()
        c_run_time.execute('''
        SELECT (MAX(circle_time) - MIN(circle_time)) FROM runner WHERE circles_id = (?)
        ''', [circles_id])
        row = c_run_time.fetchone()
        conn.commit()
        c_run_time.close()
        return row[0]

    def best_run_time(self, chat_id):
        ''' calculate best run time'''
        conn = sqlite3.connect(self.db)
        c_best_run_time = conn.cursor()
        c_best_run_time.execute('''
        SELECT MIN(maximum - minimum) FROM (
        SELECT MAX(circle_time) as maximum, MIN(circle_time) as minimum
        FROM runner
        WHERE chat_id = (?)
        GROUP BY circles_id
        )
        WHERE maximum > minimum
        ''', [chat_id])
        row = c_best_run_time.fetchone()
        conn.commit()
        c_best_run_time.close()
        return row[0]

    def circle_count(self, circles_id):
        ''' calculate count of circles'''
        conn = sqlite3.connect(self.db)
        c_circle_count = conn.cursor()
        c_circle_count.execute('''
        SELECT COUNT(circles_id) FROM runner
        WHERE circles_id = (?)
        ''', [circles_id])
        row = c_circle_count.fetchone()
        conn.commit()
        c_circle_count.close()
        return row[0]-1

    def select_circles(self, circles_id):
        ''' select circles'''
        lst = []
        conn = sqlite3.connect(self.db)
        c_select_circles = conn.cursor()
        c_select_circles.execute('''
        SELECT (circle_time) FROM runner
        WHERE circles_id = (?)
        ''', (circles_id,))
        row = (c_select_circles.fetchone())
        while row is not None:
            lst.append(row[0])
            row = c_select_circles.fetchone()
        conn.commit()
        c_select_circles.close()
        return lst
