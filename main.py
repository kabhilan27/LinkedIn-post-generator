import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post, rewrite_post
from llm_helper import llm
import re

# -------------------- INIT --------------------
if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "generated_posts" not in st.session_state:
    st.session_state.generated_posts = []

# -------------------- OPTIONS --------------------
length_options = ["Short", "Medium", "Long", "Custom"]
language_options = ["English", "Tamil", "Sinhala"]
tone_options = ["Professional", "Inspirational", "Conversational", "Humorous", "Motivational"]

# -------------------- UTIL --------------------
def extract_posts(raw_output):
    """
    Extracts post content, image idea, and hashtags from LLM output.
    Returns a list of tuples: (post_content, image_idea, hashtags)
    """
    if not isinstance(raw_output, str):
        raw_output = str(raw_output)

    pattern = r"Post\s*\d+:\s*(.*?)\s*Image Idea\s*\d+:\s*(.*?)\s*(#[^\n]+(?:\s*#[^\n]+)*)"
    matches = re.findall(pattern, raw_output, re.DOTALL)

    posts = []
    for match in matches[:3]:  # Limit to 3 posts
        post_body = match[0].strip()
        image_idea = match[1].strip()
        hashtags = match[2].strip()
        posts.append((post_body, image_idea, hashtags))
    return posts

def save_to_favorites(post, image, hashtags):
    st.session_state.favorites.append({"post": post, "image": image, "hashtags": hashtags})
    st.toast("Post saved to favorites.")

def render_post_box(text: str) -> str:
    return f"""
        <div style="
            padding: 1.2rem 1.5rem;
            margin-bottom: 1.5rem;
            border-radius: 12px;
            background-color: #ffffff10;
            border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            font-size: 1.05rem;
            line-height: 1.7;
            white-space: pre-wrap;
            color: #f5f5f5;
            text-align: left;
            font-family: 'Segoe UI', Roboto, sans-serif;
        ">
            <p style="margin: 0; font-weight: 400;">{text}</p>
        </div>
    """

def clear_favorites():
    st.session_state.favorites.clear()
    st.toast("All favorites cleared.")

# -------------------- MAIN APP --------------------
def main():
    st.set_page_config(page_title="LinkedIn Post Generator", layout="centered")
    st.markdown("<h1 style='text-align:center;'>LinkedIn Post Generator</h1>", unsafe_allow_html=True)

    fs = FewShotPosts()
    tabs = st.tabs([
        "Generate Post",
        "Rewrite Post",
        "AI Feedback",
        "Generate from Bullets"
    ])

    # -------------------- TAB 1: Generate --------------------
    with tabs[0]:
        st.markdown("### Generate LinkedIn Post")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            selected_tag = st.selectbox("Topic", options=sorted(fs.get_tags()))
        with col2:
            selected_length = st.selectbox("Post Length", options=length_options)
        with col3:
            selected_language = st.selectbox("Post Language", options=language_options)
        with col4:
            selected_tone = st.selectbox("Post Tone", options=tone_options)

        custom_line_count = None
        if selected_length == "Custom":
            custom_line_count = st.number_input("Custom line count", min_value=1, max_value=200, step=1)

        if st.button("Generate Post"):
            if custom_line_count and custom_line_count > 30:
                st.warning("⚠️ Custom line count cannot exceed 30. Please enter a value below 30.")
                st.stop()

            with st.spinner("Crafting your post..."):
                raw_output = generate_post(selected_length, selected_language, selected_tag, selected_tone, custom_line_count)

                if isinstance(raw_output, str) and raw_output.startswith("⚠️ Warning"):
                    st.warning(raw_output)
                    st.session_state.generated_posts = []
                else:
                    st.session_state.generated_posts = extract_posts(raw_output)

        if st.session_state.generated_posts:
            st.markdown("### Generated Posts")
            for i, (post, image, hashtags) in enumerate(st.session_state.generated_posts, start=1):
                st.markdown(f"#### Post {i}")
                st.markdown(render_post_box(post), unsafe_allow_html=True)
                st.markdown(f"**Hashtags:** {hashtags}")
                st.markdown(f"**Image Suggestion:** _{image}_")
                st.button(
                    f"Save Post {i} to Favorites",
                    key=f"save_btn_{i}",
                    on_click=save_to_favorites,
                    args=(post, image, hashtags)
                )

    # -------------------- TAB 2: Rewrite --------------------
    with tabs[1]:
        st.markdown("### Rewrite LinkedIn Post")

        original_post = st.text_area(
            "Paste your existing LinkedIn post",
            height=200,
            placeholder="Paste your LinkedIn post here..."
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            rewrite_length = st.selectbox("New Length", options=length_options)
        with col2:
            rewrite_language = st.selectbox("New Language", options=language_options)
        with col3:
            rewrite_tone = st.selectbox("New Tone", options=tone_options)

        custom_line_count_rewrite = None
        if rewrite_length == "Custom":
            custom_line_count_rewrite = st.number_input(
                "Custom line count (Rewrite)",
                min_value=1,
                max_value=200,
                step=1
            )

        if st.button("Rewrite Post"):
            if not original_post.strip():
                st.warning("Please paste a LinkedIn post to rewrite.")
                st.stop()

            if custom_line_count_rewrite and custom_line_count_rewrite > 30:
                st.warning("⚠️ Custom line count for rewrite cannot exceed 30. Please enter a value below 30.")
                st.stop()

            with st.spinner("Rewriting your post..."):
                rewritten = rewrite_post(
                    original_post,
                    rewrite_length,
                    rewrite_language,
                    rewrite_tone,
                    custom_line_count_rewrite
                )

            st.subheader("Rewritten Post")
            st.markdown(render_post_box(rewritten.strip()), unsafe_allow_html=True)

    # -------------------- TAB 3: AI Feedback --------------------
    with tabs[2]:
        st.markdown("### AI Feedback")

        feedback_input = st.text_area(
            "Paste your LinkedIn post for feedback",
            height=200,
            placeholder="We’ll analyze and suggest improvements..."
        )

        if st.button("Get Feedback"):
            if not feedback_input.strip():
                st.warning("Please paste a LinkedIn post to analyze.")
            else:
                with st.spinner("Analyzing your post..."):
                    prompt = f"""
Analyze the following LinkedIn post and give 3 clear and actionable tips to improve engagement. Be concise and helpful.

Post:
\"\"\"{feedback_input.strip()}\"\"\""""
                    response = llm.invoke(prompt)
                    feedback = response.content.strip()
                st.subheader("AI Suggestions")
                st.markdown(render_post_box(feedback), unsafe_allow_html=True)

    # -------------------- TAB 4: Generate from Bullets --------------------
    with tabs[3]:
        st.markdown("### Generate Post from Bullet Points")

        # Keep bullet-generated posts in session state so they persist
        if "generated_bullet_posts" not in st.session_state:
            st.session_state.generated_bullet_posts = []

        bullet_input = st.text_area(
            "Enter bullet points or rough ideas below (one per line)",
            height=200,
            placeholder="• Completed internship at XYZ\n• Learned about marketing funnels\n• Want to thank my mentor"
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            selected_language_bullet = st.selectbox("Post Language", options=language_options, key="lang_bullet")
        with col2:
            selected_tone_bullet = st.selectbox("Post Tone", options=tone_options, key="tone_bullet")
        with col3:
            selected_length_bullet = st.selectbox("Post Length", options=length_options, key="length_bullet")

        custom_line_count_bullet = None
        if selected_length_bullet == "Custom":
            custom_line_count_bullet = st.number_input("Custom line count (Bullets)", min_value=1, max_value=200,
                                                       step=1)

        if st.button("Generate from Bullets"):
            if not bullet_input.strip():
                st.warning("Please enter some bullet points to generate from.")
                st.stop()

            if custom_line_count_bullet and custom_line_count_bullet > 30:
                st.warning("⚠️ Custom line count for bullets cannot exceed 30. Please enter a value below 30.")
                st.stop()

            with st.spinner("Crafting post from your ideas..."):
                raw_output = generate_post(
                    selected_length_bullet,
                    selected_language_bullet,
                    bullet_input,
                    selected_tone_bullet,
                    custom_line_count_bullet
                )

                if isinstance(raw_output, str) and raw_output.startswith("⚠️ Warning"):
                    st.warning(raw_output)
                else:
                    st.session_state.generated_bullet_posts = extract_posts(raw_output)

        # Display stored bullet-generated posts
        if st.session_state.generated_bullet_posts:
            st.subheader("Generated Posts from Bullets")
            for i, (post, image, hashtags) in enumerate(st.session_state.generated_bullet_posts, start=1):
                st.markdown(f"#### Post {i}")
                st.markdown(render_post_box(post), unsafe_allow_html=True)
                st.markdown(f"**Hashtags:** {hashtags}")
                st.markdown(f"**Image Suggestion:** _{image}_")
                st.button(
                    f"Save Bullet Post {i} to Favorites",
                    key=f"save_bullet_btn_{i}",
                    on_click=save_to_favorites,
                    args=(post, image, hashtags)
                )

    # -------------------- SIDEBAR: FAVORITES --------------------
    with st.sidebar.expander("Saved Favorites", expanded=True):
        st.markdown("### Favorite Posts")

        if st.session_state.favorites:
            search_query = st.text_input("Search by keyword:")
            filter_tone = st.selectbox("Filter by Tone", options=["All"] + tone_options)
            filter_topic = st.selectbox("Filter by Topic", options=["All"] + sorted(fs.get_tags()))
            filter_lang = st.selectbox("Filter by Language", options=["All"] + language_options)

            def post_matches_filters(fav):
                return (
                    search_query.lower() in fav["post"].lower() and
                    (filter_tone == "All" or filter_tone.lower() in fav["post"].lower()) and
                    (filter_topic == "All" or filter_topic.lower() in fav["post"].lower()) and
                    (filter_lang == "All" or filter_lang.lower() in fav["post"].lower())
                )

            filtered_favorites = [f for f in st.session_state.favorites if post_matches_filters(f)]

            if filtered_favorites:
                for idx, fav in enumerate(filtered_favorites, start=1):
                    st.markdown(f"#### Favorite {idx}")
                    st.markdown(render_post_box(fav['post']), unsafe_allow_html=True)
                    st.markdown(f"**Hashtags:** {fav['hashtags']}")
                    st.markdown(f"*Image Suggestion:* _{fav['image']}_")
            else:
                st.warning("No favorites matched your search or filter.")

            st.button("Clear All Favorites", on_click=clear_favorites)
        else:
            st.info("No favorites saved yet.")

if __name__ == "__main__":
    main()
