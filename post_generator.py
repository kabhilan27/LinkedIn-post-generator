from llm_helper import llm
from few_shot import FewShotPosts

# Initialize few-shot helper
few_shot = FewShotPosts()


def get_length_str(length, custom_line_count=None):
    """Convert length label or custom line count to a descriptive string."""
    if length == "Custom" and custom_line_count:
        return f"Exactly {custom_line_count} lines. Each post should strictly have {custom_line_count} lines of meaningful content."
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 15 lines. Add a bit more depth and storytelling."
    if length == "Long":
        return "15 to 120 lines. Add storytelling, reflections, deep, and advice."
    return "5 to 10 lines"  # fallback


def enforce_custom_limit(length, custom_line_count):
    """Check if custom length exceeds limit."""
    if length == "Custom" and custom_line_count:
        if custom_line_count > 30:
            return "⚠️ Warning: Custom line count cannot be more than 30. Please enter 30 or fewer lines."
    return None


def get_prompt(length, language, tag, tone, custom_line_count=None):
    """Construct a prompt with clearly labeled few-shot examples and image suggestions."""
    length_str = get_length_str(length, custom_line_count)

    prompt = f"""
Generate 3 different LinkedIn posts based on the following criteria. Label them clearly as:

Post 1:
<post content>
Image Idea 1:
<image prompt>

Post 2:
<post content>
Image Idea 2:
<image prompt>

Post 3:
<post content>
Image Idea 3:
<image prompt>

No preamble or explanation.

1) Topic: {tag}
2) Language: {language}
3) Length: {length_str}
4) Tone: {tone}

If Language is "Tamil", write the posts in Tamil script.
If Language is "Sinhala", write the posts in Sinhala script.
If Language is "English", write the posts in English.

Each post must end with 2 to 4 relevant hashtags (e.g., #JobSearch, #CareerGrowth).
Hashtags should be listed on a new line after the image idea, and must be relevant to the topic and tone.
Each image idea should be specific, visual, and match the tone and topic of the post.
"""

    examples = few_shot.get_filtered_posts(length, language, tag)
    if examples:
        prompt += "\n5) Use the tone and style similar to these examples:\n"
        for i, post in enumerate(examples[:3]):
            post_text = post.get('text', '').strip()
            if post_text:
                prompt += f"\nExample {i + 1}:\n{post_text}\n"

    return prompt.strip()


def generate_post(length, language, tag, tone, custom_line_count=None):
    """Generate 3 posts and image ideas using LLM and few-shot prompting."""
    limit_check = enforce_custom_limit(length, custom_line_count)
    if limit_check:
        return limit_check

    prompt = get_prompt(length, language, tag, tone, custom_line_count)

    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        print(f"LLM failed to generate post: {e}")
        return "Error: Could not generate post."


def rewrite_post(original_text, new_length, new_language, new_tone, custom_line_count=None):
    """Rewrite an existing LinkedIn post with new tone, language, and length."""
    limit_check = enforce_custom_limit(new_length, custom_line_count)
    if limit_check:
        return limit_check

    length_str = get_length_str(new_length, custom_line_count)

    prompt = f"""
Rewrite the following LinkedIn post using the specified parameters.

Original Post:
\"\"\" 
{original_text.strip()}
\"\"\" 

New Requirements:
- Tone: {new_tone}
- Language: {new_language}
- Length: {length_str}

If Language is "Tamil", write the post in Tamil script.
If Language is "Sinhala", write the post in Sinhala script.
If Language is "English", write the post in English.

Keep the message clear, authentic, and impactful. End with 2 to 4 relevant hashtags.
No image suggestion needed.
"""

    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        print(f"LLM failed to rewrite post: {e}")
        return "Error: Could not rewrite post."
