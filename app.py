import random
from pathlib import Path
from datetime import datetime
import streamlit as st
from PIL import Image

APP_TITLE = "ほっこり褒めアプリ"
ASSETS_DIR = Path(__file__).parent / "assets" / "workers"

PRAISE_LINES = [
    "えらい。今日もちゃんと働いてる。",
    "その一手間、未来の自分が助かるやつ。",
    "焦らず丁寧。めちゃ強い。",
    "積み上げの人、いちばん信頼できる。",
    "仕事してる時点で優勝。",
    "見えない努力、ちゃんと価値ある。",
    "今日のあなた、ちゃんと頼もしい。",
    "それ、誰かの安心になってるよ。",
    "よく踏ん張ってる。ほんとに。",
    "今のペース、いい感じ。",
]

def load_images():
    if ASSETS_DIR.exists():
        return [p for p in ASSETS_DIR.glob("*") if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")]
    return []

def init_state():
    if "current_image" not in st.session_state:
        st.session_state.current_image = None
    if "last_praise" not in st.session_state:
        st.session_state.last_praise = None
    if "timestamp" not in st.session_state:
        st.session_state.timestamp = None

def pick_new_image(images):
    if images:
        st.session_state.current_image = random.choice(images)
        st.session_state.last_praise = random.choice(PRAISE_LINES)
        st.session_state.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    st.set_page_config(page_title=APP_TITLE, page_icon="🫶", layout="centered")
    init_state()

    st.title("🫶 ほっこり褒めアプリ")
    st.caption("今日のあなたへ。")

    images = load_images()

    if st.session_state.current_image is None:
        pick_new_image(images)

    if st.session_state.current_image:
        img = Image.open(st.session_state.current_image)
        st.image(img, use_container_width=True)

        st.markdown("### 👏")
        st.markdown(f"## {st.session_state.last_praise}")
        st.write(f"🕒 {st.session_state.timestamp}")

    else:
        st.warning("assets/workers フォルダに画像を入れてください")

    st.divider()

    if st.button("🔁 もう一人見る"):
        pick_new_image(images)
        st.rerun()

if __name__ == "__main__":
    main()