class TestConfig:
    SQLALCHEMY_DATABASE_URI = 'postgresql:///blogly_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Use test database and don't clutter tests with SQL
    SQLALCHEMY_ECHO = False
     # Make Flask errors be real errors, ratehr than HTML pages with error info
    TESTING = True
    # This is a bit of hack, but don't use Flask DebugToolbar
    DEBUG_TB_HOSTS = ['dont-show-debug-toolbar']
    # other configuration options for testing...
