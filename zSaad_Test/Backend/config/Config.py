import os
audio_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
audio_dir = os.path.join(audio_dir, 'Frontend')
audio_dir = os.path.join(audio_dir, 'static')
audio_dir = os.path.join(audio_dir, 'audio')
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MONGO_DBNAME = 'zSaad_Test'
    MONGO_URI = 'mongodb://localhost:27017/zSaad_Test'
    AUDIO_FOLDER = audio_dir
    MAX_CONTENT_LENGTH = 1024*1024