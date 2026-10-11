
import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="NatureQuest AI", page_icon="🌿")

st.title("🌿 NatureQuest AI")
st.write("Less screen time. More real-world adventures.")

time_available = st.selectbox(
    "How much free time do you have?",
    ["10 minutes", "20 minutes", "30 minutes", "1 hour"]
)

interest = st.selectbox(
    "What do you enjoy?",
    ["Nature walks", "Birdwatching", "Gardening", "Photography"]
)

ACTIVITIES = {
    "Nature walks": {
        "title": "The Five-Senses Nature Walk",
        "steps": [
            "Walk along a safe, familiar path.",
            "Notice three different leaf shapes and two natural sounds.",
            "Pick one detail to photograph or sketch; leave nature untouched."
        ],
        "benefit": "Builds observation skills while encouraging time outdoors."
    },
    "Birdwatching": {
        "title": "Backyard Bird Detective",
        "steps": [
            "Find a safe spot where birds can be observed quietly.",
            "Watch for a few minutes and note bird colours or calls.",
            "Record your observations without disturbing nests or wildlife."
        ],
        "benefit": "Helps you notice local biodiversity."
    },
    "Gardening": {
        "title": "A Tiny Garden Mission",
        "steps": [
            "Choose a plant you already have or a small garden area.",
            "Check the soil and water only if the plant needs it.",
            "Remove a few weeds if appropriate and observe new growth."
        ],
        "benefit": "Encourages care for plants and greener spaces."
    },
    "Photography": {
        "title": "Nature's Pattern Hunt",
        "steps": [
            "Look for a safe outdoor spot with interesting natural details.",
            "Photograph patterns in leaves, clouds, bark or flowers.",
            "Choose your favourite photo and write one sentence about it."
        ],
        "benefit": "Builds creativity and appreciation for the natural world."
    }
}

if st.button("Discover my outdoor adventure"):
    with st.spinner("Asking the open-source AI for inspiration..."):
        try:
            generator = pipeline(
                "text2text-generation",
                model="google/flan-t5-small"
            )

            prompt = (
                f"Suggest a creative outdoor activity about {interest}. "
                f"Available time: {time_available}. "
                "Give a short activity name and one sentence describing it."
            )

            result = generator(
                prompt,
                max_new_tokens=60,
                do_sample=False,
                repetition_penalty=1.5,
                no_repeat_ngram_size=3,
                truncation=True
            )

            ai_idea = result[0]["generated_text"].strip()

        except Exception:
            ai_idea = ""

    activity = ACTIVITIES[interest]

    st.subheader(activity["title"])

    if ai_idea and len(ai_idea.split()) >= 5:
        st.markdown("**AI inspiration**")
        st.write(ai_idea)

    st.markdown("**Your adventure plan**")
    for index, step in enumerate(activity["steps"], start=1):
        st.write(f"{index}. {step}")

    st.info(f"🌱 Nature benefit: {activity['benefit']}")
    st.caption(
        "AI-generated ideas can be imperfect. Follow local safety rules "
        "and avoid disturbing plants or wildlife."
    )
