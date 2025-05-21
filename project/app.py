from flask import Flask, render_template, session, redirect, url_for, request
import requests

app = Flask(__name__)

app.secret_key = "Cats18273645"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        tag = request.form.get("tag")
        if tag:
            return redirect(url_for("filter", tag=tag))
        
    try:
        response = requests.get("https://cataas.com/api/cats?limit=100")
        cats = response.json()
        cat_data = []
    except requests.exceptions.HTTPError as HTTPError:
        return render_template("error.html", error = f"HTTP Error: {HTTPError}")
    else:
        for cat in cats:
            try:
                id = cat["id"]
                filetype = cat["mimetype"].replace("image/", "")
                image_url = f"https://cataas.com/cat/{id}.{filetype}"
                date = cat["createdAt"]
                tags = cat["tags"]

                cat_data.append({
                    'id': id,
                    'image': image_url,
                    'filetype': filetype,
                    'date': date,
                    'tags': tags
                })
            except KeyError:
                continue
                
        session['cat_details'] = cat_data
        
        return render_template("index.html", cat_data = cat_data) 

@app.route("/cats/<int:id>")
def cat(id):
    try:
        cat_data = session.get("cat_details")
        this_cat = cat_data[id]
    except None:
        return render_template("error.html", error = "Cats not loaded. Return to the homepage.")
    except KeyError:
        return render_template("error.html", error = "Session Key Error")
    else:
        return render_template("cat.html", this_cat = this_cat)

@app.route("/filter/<string:tag>", methods = ["GET", "POST"])
def filter(tag):
    if request.method == "POST":
        tag = request.form.get("tag")
        if tag:
            return redirect(url_for("filter", tag=tag))
    
    try:
        response = requests.get("https://cataas.com/api/cats?limit=1987")
        cats = response.json()
        cat_data = []
    except requests.exceptions.HTTPError as HTTPError:
        return render_template("error.html", error = f"HTTP Error: {HTTPError}")
    else:
        for cat in cats:
            try:
                tags = cat["tags"]
                if tag in tags:
                    id = cat["id"]
                    filetype = cat["mimetype"].strip("image/")
                    image_url = f"https://cataas.com/cat/{id}.{filetype}"
                    date = cat["createdAt"]

                    cat_data.append({
                        'id': id,
                        'image': image_url,
                        'filetype': filetype,
                        'date': date,
                        'tags': tags
                    })             
            except KeyError:
                continue

        session["tagged_cat_details"] = cat_data

        return render_template("index.html", cat_data = cat_data) 

if __name__ == '__main__':

    app.run(debug=True)