from flask import Flask, request, render_template, send_file
import main
import os

app=Flask(__name__)

@app.route('/', methods =["GET", "POST"])
def home():
    if request.method == "POST":
        url=request.form.get("spotify_url")
        dfile=main.execute(url)
        if dfile and os.path.exists(dfile):
            return send_file(dfile, as_attachment=True)
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)