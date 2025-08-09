import json
import re
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm


# ✅ Remove emojis and unsupported Unicode
def clean_text(text):
    return text.encode('utf-8', 'ignore').decode('utf-8')


# ✅ Detect language override using Sinhala/Tamil Unicode ranges
def detect_language_override(text):
    if re.search(r'[\u0D80-\u0DFF]', text):  # Sinhala script
        return "Sinhala"
    elif re.search(r'[\u0B80-\u0BFF]', text):  # Tamil script
        return "Tamil"
    return "English"


# ✅ Extract metadata using LLM with override
def extract_metadata(post):
    template = '''
    You are given a LinkedIn post. You need to extract:
    - number of lines
    - language (English, Tamil, or Sinhala)
    - tags (max 2 relevant topics)

    Definitions:
    - Tamil = post is written using Tamil script
    - Sinhala = post is written using Sinhala script

    Return a valid JSON with exactly these three keys: line_count, language, tags.
    No preamble.

    Post:
    {post}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={'post': post})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
        # ✅ Override LLM's guess with regex detection if needed
        res['language'] = detect_language_override(post)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return res


# ✅ Create a unified set of tags using LLM
def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])

    unique_tags_list = ', '.join(unique_tags)

    template = '''You are given a list of tags. Your task is to unify and standardize them:

    1. Merge similar or related tags into general tags.
    2. Use Title Case.
    3. Return valid JSON with original tag → unified tag. No explanation.

    Example:
    {{
      "Job Hunting": "Job Search",
      "Motivation": "Motivation"
    }}

    Tags:
    {tags}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": str(unique_tags_list)})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse tags.")
    return res


# ✅ Main processing function
def process_posts(raw_file_path, processed_file_path="data/processed_posts.json"):
    enriched_posts = []

    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)

        for post in posts:
            post['text'] = clean_text(post['text'])
            metadata = extract_metadata(post['text'])

            # ✅ Debug prints
            print("Detected language:", metadata["language"])
            print("Extracted tags:", metadata["tags"])
            print("Line count:", metadata["line_count"])
            print("Post:", post["text"])
            print("=" * 50)

            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)

    # ✅ Standardize tags
    unified_tags = get_unified_tags(enriched_posts)

    for post in enriched_posts:
        current_tags = post['tags']
        new_tags = {unified_tags.get(tag, tag) for tag in current_tags}
        post['tags'] = list(new_tags)

    # ✅ Save output
    with open(processed_file_path, encoding='utf-8', mode="w") as outfile:
        json.dump(enriched_posts, outfile, indent=4)


if __name__ == '__main__':
    process_posts("data/raw_posts.json", "data/processed_posts.json")
