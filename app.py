# learning flask for web development

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def main_page():
    return "hello world"
    
@app.route('/login')
def login_page():
    return render_template("index.html")
    
if __name__ == '__main__':
    app.run(debug = True)