from zDB_Tutorial.Backend.app import APP_MAIN


if (__name__ == "__main__"):
    print(APP_MAIN.config['SECRET_KEY'])
    APP_MAIN.run(debug=True)

