from flask_socketio import SocketIO
from flask_session import Session
# from flask_redis import FlaskRedis
from flask import Flask

from app.user import User


app = Flask(__name__)


class Config:
    # DEBUG调试模式
    DEBUG = True
    # json多字节转unicode编码
    # JSON_AS_ASCII = False
    # 数据库链接配置
    SECRET_KEY = "FEICHANGANQUANDEMIYAO"
    # session存储方式为redis
    SESSION_TYPE = "filesystem"
    # session保存数据到redis时启用的链接对象
    # SESSION_REDIS = FlaskRedis(host='localhost', port=6379, db=1, decode_responses=True)
    # # 如果设置session的生命周期是否是会话期, 为True，则关闭浏览器session就失效
    # SESSION_PERMANENT = False
    # # 是否对发送到浏览器上session的cookie值进行加密
    # SESSION_USE_SIGNER = True
    # 保存到redis的session数的名称前缀
    # SESSION_KEY_PREFIX = "FlaskR"
    # # redis的链接配置
    # REDIS_URL = "redis://localhost:6379/0"


User.load()

app.config.from_object(Config)
# redis.init_app(app)
Session(app)
socketio = SocketIO(app, manage_session=False)

rooms = {}
