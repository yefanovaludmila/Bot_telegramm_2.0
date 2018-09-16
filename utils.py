''' Utils file '''
import configparser
import logging

class Utils:
    ''' class Utils '''
    def __init__(self, filename):
        ''' init utils file '''
        self.config = configparser.ConfigParser()
        self.config.read(filename)

    def get_token(self):
        ''' get token '''
        return self.config['telegram']['token']

    def get_url(self):
        ''' get url '''
        return self.config['telegram']['url']

    def  get_logger(self):
        ''' get logger '''
        level = getattr(
            logging,
            self.config['common']['loglevel'].upper(),
        )
        logfile = self.config['common']['logfile']
        logger = logging.getLogger('telegramm_bot')
        logger.setLevel(level)

        fh_logger = logging.FileHandler(logfile)
        formatter = logging.Formatter('%(filename)s[LINE:%(lineno)d]# %(name)s '
                                      '%(levelname)-8s [%(asctime)s]  %(message)s')
        fh_logger.setFormatter(formatter)

        logger.addHandler(fh_logger)
        return logger
