from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world(user=None):
    user = user or 'suzie q'
    return render_template('index.html', user=user)

if __name__ == '__main__':
    app.run()
