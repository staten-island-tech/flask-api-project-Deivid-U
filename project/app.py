from flask import Flask, render_template, session, redirect, url_for, request
import requests

app = Flask(__name__)

app.secret_key = "Cats18273645"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        entered_tag = request.form.get("tag")
        if entered_tag:
            return redirect(url_for("filter", tag = entered_tag))
        
    try:
        response = requests.get("https://cataas.com/api/cats?limit=50", timeout = 10)
        response.raise_for_status()       
        cats = response.json()
    except requests.exceptions.HTTPError as http_error:
        return render_template("error.html", error = f"HTTP Error: {http_error}")
    except requests.exceptions.RequestException as request_error:
        return render_template("error.html", error = f"Request Error: {request_error}")
    except ValueError as json_error:
        return render_template("error.html", error = f"Invalid JSON: {json_error}")
    else:
        cat_data = []

        for cat in cats:
            try:
                id = cat["id"]
                filetype = cat["mimetype"].replace("image/", "")
                image_url = f"https://cataas.com/cat/{id}"
                created_at = cat["createdAt"]
                tags = cat["tags"]

                cat_data.append({
                    'id': id,
                    'image_url': image_url,
                    'filetype': filetype,
                    'created_at': created_at,
                    'tags': tags
                })
            except KeyError:
                continue #if any individual cat is not formatted properly the code just keeps iterating
                
        if len(cat_data) > 0:
            session['cat_details'] = cat_data
            return render_template("index.html", cat_data = cat_data) 
        else: #if every single cat was not formatted properly it loads an error page
            return render_template("error.html", error = "No valid data was retrieved from the API.")

@app.route("/cats/<string:id>")
def cat(id):
    cat_data = session.get("cat_details")
    
    if cat_data is None:
        return render_template("error.html", error = "No cat data found in session. Click on the header to return to the homepage.")
    else:
        try:
            this_cat = next(cat for cat in cat_data if cat["id"] == id)
        except StopIteration:
            return render_template("error.html", error = "Cat not found.")
        except TypeError:
            return render_template("error.html", error = "Invalid cat data in session.")
        else:
            return render_template("cat.html", this_cat = this_cat)

@app.route("/filter/<string:tag>", methods = ["GET", "POST"])
def filter(tag):
    if request.method == "POST":
        entered_tag = request.form.get("tag")
        if entered_tag:
            return redirect(url_for("filter", tag = entered_tag))
    
    try:
        response = requests.get("https://cataas.com/api/cats?limit=1987") #limit is equal to the total # of cats in the API to ensure we get every result for more obscure tags
        response.raise_for_status()
        cats = response.json()
    except requests.exceptions.HTTPError as http_error:
        return render_template("error.html", error = f"HTTP Error: {http_error}")
    except requests.exceptions.RequestException as request_error:
        return render_template("error.html", error = f"Request Error: {request_error}")
    except ValueError as json_error:
        return render_template("error.html", error = f"Invalid JSON: {json_error}")
    else:
        cat_data = []

        for cat in cats:
            try:
                tags = cat["tags"] #the API's tags are sensitive to capitalization (eg. "Angry" and "angry" are different tags), so I am not using .lower() as to maintain the API's tag system

                if tag in tags and len(cat_data) <= 50: #because all cats are retrieved for filtering in this page, the total number of cats for a given tag is capped at 50 to fit the data in the session cookie
                    id = cat["id"]
                    filetype = cat["mimetype"].strip("image/")
                    image_url = f"https://cataas.com/cat/{id}"
                    created_at = cat["createdAt"]

                    cat_data.append({
                        'id': id,
                        'image_url': image_url,
                        'filetype': filetype,
                        'created_at': created_at,
                        'tags': tags
                    })             
            except KeyError:
                continue #keeps iterating if an individual cat is improperly formatted

        if len(cat_data) > 0:
            session['cat_details'] = cat_data
            return render_template("index.html", cat_data = cat_data) 
        else: #if every single cat was not formatted properly it loads an error page
            return render_template("error.html", error = "No valid data was retrieved from the API. Try searching for a different tag, and note that tags are sensitive to capitaliztion.")

if __name__ == '__main__':

    app.run(debug=True)