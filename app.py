from flask import Flask

from route.user import user

app = Flask(__name__)
app.register_blueprint(user)
app.config['JSON_AS_ASCII'] = False

if __name__ == '__main__':
    app.run()
