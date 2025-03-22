# app.py
from flask import Flask, render_template, send_from_directory
import os, threading, time
from insta_watcher import check_for_new_post

app = Flask(__name__)
PHOTO_FOLDER = "downloaded_photos"

# 10분마다 새 게시물 확인
def run_periodic_checker(interval=600):
    def loop():
        while True:
            print("🔍 인스타 새 게시물 확인 중...")
            try:
                check_for_new_post()
            except Exception as e:
                print("오류 발생:", e)
            time.sleep(interval)
    thread = threading.Thread(target=loop)
    thread.daemon = True
    thread.start()

@app.route("/")
def gallery():
    images = [f for f in os.listdir(PHOTO_FOLDER) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    images.sort(reverse=True)
    return render_template("gallery.html", images=images)

@app.route("/photos/<filename>")
def photo(filename):
    return send_from_directory(PHOTO_FOLDER, filename)

if __name__ == "__main__":
    run_periodic_checker()
    app.run(debug=True)
