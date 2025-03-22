# insta_watcher.py
import instaloader, os, json, glob

def check_for_new_post():
    TARGET_USERNAME = "yezyizhere"
    SAVE_FOLDER = "downloaded_photos"
    DATA_FILE = "last_post.json"

    L = instaloader.Instaloader(
        download_videos=False,
        download_video_thumbnails=False,
        save_metadata=False,
        download_comments=False
    )

    os.makedirs(SAVE_FOLDER, exist_ok=True)

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            last_saved_id = json.load(f).get("last_post_id")
    else:
        last_saved_id = None

    profile = instaloader.Profile.from_username(L.context, TARGET_USERNAME)
    latest_post = next(profile.get_posts())
    latest_id = latest_post.mediaid

    if str(latest_id) != str(last_saved_id):
        print("📸 새 게시물 발견! 저장 중...")
        L.download_post(latest_post, target=SAVE_FOLDER)

        txt_files = glob.glob(os.path.join(SAVE_FOLDER, '*.txt'))
        for file in txt_files:
            os.remove(file)

        with open(DATA_FILE, "w") as f:
            json.dump({"last_post_id": latest_id}, f)
    else:
        print("✅ 새 게시물 없음")
