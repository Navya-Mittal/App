import json, random
import streamlit as st

st.set_page_config(page_title="memory app", layout="centered")

@st.cache_data
def load(name):
    with open(f"data/{name}.json") as f:
        return json.load(f)

questions = load("question_bank")
gifs = load("reaction_gif_bank")
weird_lines = load("weird_face_alternatives")
tricks = load("easter_egg_tricks")

emotions = sorted({q["emotion_category"] for q in questions})

st.title("today's memory")

# step 1: mood check-in
mood = st.selectbox("how are you feeling today?", emotions)

# step 2: pick an unused question for that mood, mark it used
pool = [q for q in questions if q["emotion_category"] == mood and q["used_count"] == 0]
if not pool:
    pool = [q for q in questions if q["emotion_category"] == mood]
question = random.choice(pool)
question["used_count"] += 1

st.subheader(question["phrasing"])
answer = st.text_input("your answer")

# step 3: media type choice
media_type = st.radio("want a photo, video, or painting?", ["photo", "video", "painting"], horizontal=True)

if st.button("show me a memory"):
    # placeholder "photo" block — swap this for your real photo/story dataset lookup
    st.markdown("---")
    st.caption("age 22 · summer, 2019")
    st.image("https://placehold.co/500x400?text=" + media_type, use_container_width=True)
    st.write("remember how hot that day was? ps — that face still looks weird.")

    # step 4: reaction gif tagged to the mood
    gif_pool = [g for g in gifs if g["sentiment_tag"] == mood] or gifs
    gif = random.choice(gif_pool)
    st.caption(f"reaction: {gif['fallback_style']}  (gif query: \"{gif['search_query']}\")")

    # step 5: one "weird face" alternative line, just to show it's wired up
    st.info(random.choice(weird_lines)["line"])

    # step 6: occasional easter egg trigger (10% chance, capped by max_triggers in a real session)
    if random.random() < 0.1:
        trick = tricks[0]
        st.warning(f"easter egg: {trick['name']} — {trick['closing_line']}")

st.markdown("---")
st.caption(f"{len(questions)} questions · {len(gifs)} gif tags · {len(weird_lines)} alt lines · {len(tricks)} tricks loaded")
