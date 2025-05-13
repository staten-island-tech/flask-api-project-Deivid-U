from flask import Flask, render_template, session
import requests

app = Flask(__name__)

app.secret_key = "Cats18273645"

@app.route("/")
def index():
    
    try:
        response = requests.get("https://cataas.com/api/cats?limit=100")
        cats = response.json()
        cat_pics = []
    except requests.exceptions.HTTPError as HTTPError:
        return render_template("error.html", error = f"HTTP Error: {HTTPError})
    else:
        for cat in cats:
            try:
                id = cat["id"]
                filetype = cat["mimetype"].strip("image/")
                image_url = f"https://cataas.com/cat/{id}.{filetype}"
                date = cat["createdAt"]
            except KeyError:
                continue
            else:
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
    try:
        cat_pics = session.get("cat_details")
        this_cat = cat_pics[id]
    except None:
        return render_template("error.html", error = "Cats not loaded. Return to the homepage.")
    except KeyError:
        return render_template("error.html", error = "Session Key Error")
    else:
        return render_template("cat.html", this_cat = this_cat)

if __name__ == '__main__':

    app.run(debug=True)