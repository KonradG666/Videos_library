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
def video_update(video_id):
    video = videos.get(video_id - 1)
    form = MusicVideoLibrary(data=video)

    if request.method == "POST":
        if form.validate_on_submit():
           videos.update(video_id - 1, form.data)
        return redirect(url_for("videos_list"))
    return render_template("music_upd.html", form=form, video_id=video_id)


@app.route("/library/delete/<int:video_id>", methods=["GET"])
def delete_video(video_id):
    form = MusicVideoLibrary()
    video = videos.delete(video_id - 1)
    error = ""
    if not video:
        abort(404)

    return render_template("music_del.html", form=form, video_id=video_id, error=error)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


if __name__ == "__main__":
    app.run(debug=True)
