import os
import threading

class GlobalConf():
    # Here will be the instance stored.

    GOOGLE_CLIENT_ID = '375961356325-p3umdlkkjr6ak9kairqv8b3ttalio52a.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = '8UggTqBUxM3M-9cd8KtLv8Tj'
    REDIRECT_URI = '/oauth2callback'

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MONGO_DBNAME = 'zSaad_Test'
    MONGO_URI = 'mongodb://localhost:27017/zSaad_Test'

    audio_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    audio_dir = os.path.join(audio_dir, 'Frontend')
    audio_dir = os.path.join(audio_dir, 'static')
    audio_dir = os.path.join(audio_dir, 'audio')

    AUDIO_FOLDER = audio_dir
    MAX_CONTENT_LENGTH = 1024 * 1024

    template_folder = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    template_folder = os.path.join(template_folder, 'Frontend')
    template_folder = os.path.join(template_folder, 'templates')

    static_folder = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    static_folder = os.path.join(static_folder, 'Frontend')
    static_folder = os.path.join(static_folder, 'static')


    __instance = None
    lock = threading.Lock()

    def __init__(self):
        self.data = None
        print(GlobalConf.template_folder)
        print(GlobalConf.static_folder)
        print(GlobalConf.audio_dir)


    @staticmethod
    def getInstance():
        """ Static access method. """
        GlobalConf.lock.acquire()
        if GlobalConf.__instance == None:
            GlobalConf.__instance = GlobalConf()
        GlobalConf.lock.release()
        return GlobalConf.__instance

    def setData(self, data):
        self.data = data
