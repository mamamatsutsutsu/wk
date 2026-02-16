import random
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from datetime import datetime
import streamlit as st
from PIL import Image
from st_clickable_images import clickable_images

APP_TITLE = "Praise Workers"
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

WORK_HINTS = [
    "資料づくり",
    "顧客対応",
    "調整",
    "分析",
    "コーディング",
    "会議",
    "運用監視",
]

@dataclass
class Worker:
    name: str
    path: Path

def load_workers() -> List[Worker]:
    if ASSETS_DIR.exists():
        imgs = [p for p in ASSETS_DIR.glob("*") if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")]
        if imgs:
            return [Worker(name=p.stem, path=p) for p in imgs]
    return [Worker(name=f"Worker{i}", path=ASSETS_DIR / f"worker{i}.png") for i in range(1,5)]

def to_data_url(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    img = Image.open(path)
    import io, base64
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{b64}"

def init_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "last" not in st.session_state:
        st.session_state.last = None

def make_praise():
    base = random.choice(PRAISE_LINES)
    hint = random.choice(WORK_HINTS)
    return f"{base}（{hint}、いい感じ）"

def main():
    st.set_page_config(page_title=APP_TITLE, page_icon="🫶", layout="wide")
    init_state()

    st.title("🫶 ほっこり褒めアプリ")
    st.caption("働いてる人をクリック → その瞬間の時間と一緒に褒めます")

    workers = load_workers()
    data_urls = []
    titles = []

    for w in workers:
        u = to_data_url(w.path)
        if u is None:
            u = "https://via.placeholder.com/400x300?text=Worker"
        data_urls.append(u)
        titles.append(w.name)

    clicked = clickable_images(
        data_urls,
        titles=titles,
        div_style={"display": "grid", "gridTemplateColumns": "repeat(3, 1fr)", "gap": "12px"},
        img_style={"borderRadius": "16px", "cursor": "pointer"},
    )

    if clicked is not None and int(clicked) >= 0:
        now = datetime.now()
        timestamp_full = now.strftime("%Y-%m-%d %H:%M:%S")
        who = titles[int(clicked)]
        msg = make_praise()

        st.session_state.last = {
            "who": who,
            "msg": msg,
            "time": timestamp_full
        }

        st.session_state.history.insert(0, st.session_state.last)

    col1, col2 = st.columns([0.6, 0.4])

    with col2:
        st.subheader("Your praise")
        if st.session_state.last:
            st.markdown(f"### {st.session_state.last['msg']}")
            st.write(f"🕒 {st.session_state.last['time']}")
            st.write(f"for: {st.session_state.last['who']}")
        else:
            st.info("左の画像をクリックしてね")

        st.divider()
        st.subheader("History")
        for h in st.session_state.history[:10]:
            st.write(f"{h['time']} - {h['who']} - {h['msg']}")

if __name__ == "__main__":
    main()