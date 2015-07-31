import traceback
from application import Application

DEBUG = True

if __name__ == '__main__':
    try:
        app = Application()
        app.run()
    except Exception as e:
        if DEBUG:
            print(traceback.print_exc())
        else:
            print(str(e))
