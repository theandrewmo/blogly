class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql:///blogly'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SECRET_KEY = 'not-very-secret'
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    # other configuration options...
