from flask import Flask, request, render_template, redirect, url_for
from forms import MusicVideoLibrary
from data import videos

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/library/", methods=["GET", "POST"])
def videos_list():
    form = MusicVideoLibrary()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            videos.create(form.data)
            videos.save_all()
        return redirect(url_for("videos_list"))

    return render_template("music.html", form=form, videos=videos.all(), error=error)


@app.route("/library/<int:video_id>/", methods=["GET", "POST"])
def video_details(video_id):
    video = videos.get(video_id - 1)
    form = MusicVideoLibrary(data=video)

    if request.method == "POST":
        if form.validate_on_submit():
            videos.update(video_id - 1, form.data)
        return redirect(url_for("todos_list"))
    return render_template("music_id.html", form=form, todo_id=todo_id)


if __name__ == "__main__":
    app.run(debug=True)
