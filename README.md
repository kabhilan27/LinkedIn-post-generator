# 💼 LinkedIn Post Generator

An **AI-powered LinkedIn content creation tool** built with **Python** and **Streamlit** that enables professionals, content creators, and job seekers to effortlessly craft **engaging, high-quality LinkedIn posts**.  

Whether you want to **generate new posts**, **rewrite existing ones**, **receive AI feedback**, or **transform bullet points into polished content**, this tool has you covered — with multilingual support and built-in image suggestions.

---

## 🛠 Tech Stack
- **Python** 🐍 – Core programming language
- **Streamlit** 📊 – Interactive web app framework
- **Groq API** 🤖 – LLM-powered text generation
- **NumPy** 🔢 – Backend processing
- **dotenv** 🔐 – Secure API key management

---

## ✨ Features

**📝 Post Generation**
- Generate exactly **3 unique, high-quality LinkedIn posts** per request  
- Supports **English**, **Tamil**, and **Sinhala**  
- Customize **length**, **tone**, and **hashtags** for each post  
- Automatically appends **relevant hashtags** and **AI-generated image suggestions**  
- Ideal for **content planners** and **personal branding**

**✍️ Rewrite Posts**
- Improve clarity, tone, and engagement level of an existing post  
- Supports **tone switching** (formal, casual, motivational, etc.)  
- Adjust **length** with a custom line limit (**max 30 lines**)  
- Useful for **repurposing older content**

**🤖 AI Feedback**
- Paste your LinkedIn post and get **3 actionable suggestions**  
- AI evaluates **engagement potential**, **structure**, and **tone**  
- Helps you **optimize for reach** and **professional impact**

**📌 Bullet-to-Post Conversion**
- Paste bullet points or raw ideas  
- AI transforms them into a **polished, ready-to-post LinkedIn article**  
- Includes **hashtags** and **image prompts** automatically  
- Supports multilingual content creation

**⭐ Favorites**
- Save your best posts locally for **future reuse**  
- Quickly **copy content** with one click  
- Great for maintaining a **content library**

---

## 💡 Use Cases
- **Job Seekers** – Stand out with impactful personal branding posts  
- **Freelancers** – Showcase portfolio and work updates  
- **Marketers** – Generate campaign content quickly  
- **Thought Leaders** – Maintain a consistent posting schedule  
- **Multilingual Professionals** – Post in English, Tamil, and Sinhala with ease  

---

## 🚀 How to Run Locally

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/linkedin-post-generator.git
   cd linkedin-post-generator
   ```

2. **Install Dependencies**
   ```bash
   pip install streamlit python-dotenv groq numpy 
   ```

3. **Set up Environment Variables**
   - Create a `.env` file in the root directory  
   - Add your Groq API key:  
     ```
     GROQ_API_KEY=your_api_key_here
     ```

4. **Run the App**
   ```bash
   streamlit run main.py
   ```

---

## 📜 License
This project is licensed under the **MIT License** – feel free to use, modify, and share.

---
