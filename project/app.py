from flask import Flask, render_template, session
import requests

app = Flask(__name__)

app.secret_key = "Cats18273645"

@app.route("/")
def index():
    response = requests.get("https://cataas.com/api/cats?limit=100")
    cats = response.json()
    cat_pics = []
    
    for cat in cats:
        id = cat["id"]
        filetype = cat["mimetype"].strip("image/")
        image_url = f"https://cataas.com/cat/{id}.{filetype}"
        date = cat["createdAt"]

        cat_pics.append({
            'id': id,
            'image': image_url,
            'filetype': filetype,
            'date': date
        })

    session['cat_details'] = cat_pics
    
    return render_template("index.html", cat_pics = cat_pics) 

@app.route("/cats/<int:id>")
def cat(id):
    cat_pics = session.get["cat_details"]
    this_cat = cat_pics[id]

    return render_template("cat.html", this_cat = this_cat)


if __name__ == '__main__':

    app.run(debug=True)