from devfun import app

@app.route('/')
def hello():
    return "Goodbye!"


@app.route('/<name>')
def hi(name):
    return "Goodbye! {}".format(name)
