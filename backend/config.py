USERNAME = "root"  # 每个人设置的名字和账号会不同，这里是自己设定的账号密码
PASSWORD = "Ch13267778582"  # 每个人设置的名字和账号会不同，这里是自己设定的账号密码
HOST = 'localhost'
PORT = '11451'
DATABASE = 'bupt'  #这里是数据库名
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True