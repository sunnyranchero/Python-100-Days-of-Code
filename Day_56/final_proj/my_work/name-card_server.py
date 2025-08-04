from flask import Flask, render_template
# This is the "Final Project on this day"

# init class
app = Flask(__name__)

# define a home page
@app.route("/")
def home():
    return render_template("index.html")

# Enable launching server from file run
if __name__ == "__main__":
    app.run(debug=True)
