from flask import Flask,render_template
import os


template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'Frontend')
template_dir = os.path.join(template_dir, 'templates')
print(template_dir,"asd")
app = Flask(__name__,template_folder=template_dir)


@app.route('/')
def hello_world():
    return render_template("dummy.html")


if __name__ == '__main__':
    app.run(debug=True)
