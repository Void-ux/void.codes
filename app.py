from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        print(request.json)


@app.route('/chiefron')
def chief_ron():
    return render_template('chief_ron.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ =='__main__':
    app.run(host='0.0.0.0')
