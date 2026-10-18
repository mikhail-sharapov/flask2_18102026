class Config:
    TESTING = True


class ProductionConfig(Config):
    SECRET_KEY = "307778ecdb2dd00d6fe8a70cc4d04d30893339247adb005696c19bfe3ac822cc"


class DevelopmentConfig(Config):
    SECRET_KEY = "my_secret_key"


