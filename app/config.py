class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/medicals'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'khue'  # Thay đổi thành secret key của bạn
