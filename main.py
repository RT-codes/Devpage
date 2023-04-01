from flask import Flask, render_template

app = Flask(__name__)

#link variable for url_for




@app.route('/')
def index():
    return render_template( 'home.html' )

if __name__ == '__main__':
    app.run(port=5000)
