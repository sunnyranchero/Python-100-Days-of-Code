from flask import Flask, render_template

# init the class object
app = Flask(__name__)

# Define the routing functions and decorate

@app.route("/")
def home():
    return render_template("index.html")

# set up project to run off this file.
if __name__ == "__main__":
    app.run(debug=True)


