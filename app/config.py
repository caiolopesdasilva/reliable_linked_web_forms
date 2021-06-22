class Config(object):
    TESTING = False
    DEBUG = False


class Development(Config):
    DEBUG = True


class TESTING(Config):
    TESTING = True
    DEBUG = False
