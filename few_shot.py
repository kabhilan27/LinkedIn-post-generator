import json
import pandas as pd


class FewShotPosts:
    def __init__(self, file_path="data/processed_posts.json"):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)

    def load_posts(self, file_path):
        try:
            with open(file_path, encoding="utf-8") as f:
                posts = json.load(f)
                self.df = pd.json_normalize(posts)

                # Categorize length for each post
                self.df["length"] = self.df["line_count"].apply(self.categorize_length)

                # Extract unique tags from all posts
                all_tags = self.df['tags'].dropna().apply(lambda x: x if isinstance(x, list) else []).sum()
                self.unique_tags = set(all_tags)

        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {file_path}")

    def categorize_length(self, line_count):
        try:
            if line_count < 5:
                return "Short"
            elif 5 <= line_count <= 10:
                return "Medium"
            else:
                return "Long"
        except Exception:
            return "Unknown"

    def get_tags(self):
        return self.unique_tags or set()

    def get_filtered_posts(self, length, language, tag):
        if self.df is None:
            print("Data not loaded properly.")
            return []

        df_filtered = self.df[
            (self.df['language'] == language) &
            (self.df['length'] == length) &
            (self.df['tags'].apply(lambda tags: isinstance(tags, list) and tag in tags))
        ]
        return df_filtered.to_dict(orient="records")


if __name__ == "__main__":
    fs = FewShotPosts()
    posts = fs.get_filtered_posts("Medium", "English", "Job Search")

    for post in posts:
        print(json.dumps(post, indent=2))
