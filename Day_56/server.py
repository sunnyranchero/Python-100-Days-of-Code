from flask import Flask, render_template

# Init the class
app = Flask(__name__)

# Render the home page (example)
@app.route("/")
def home():
    # return "<h1 style='color:SlateBlue;'><u>Welcome home</u></h1>"
    return render_template("index.html")
    # I kept the old code to be able to research it later on or ref for later projects.
    # return render_template("angela cv.html")

# to get images to work, they must be in the static folder. Subfolders there do not matter much



# if you run this code from here, you don't need to change the env variables
if __name__ == "__main__":
    app.run(debug=True)

