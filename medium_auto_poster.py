import streamlit as st
import openai
import requests
import random

openai.api_key = st.secrets["OPENAI_API_KEY"]
medium_token = st.secrets["MEDIUM_TOKEN"]

topics = [
    "How I Found My First Internship",
    "Lessons from 10 Job Rejections",
    "What No One Tells You About Graduate Roles"
]

def generate_post(topic):
    prompt = f"""Write a Medium blog post on the topic: "{topic}". 
Make it inspirational, aimed at engineering students looking for internships or graduate jobs. Use headings, storytelling, and end with a helpful call to action."""
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def post_to_medium(title, content):
    headers = {"Authorization": f"Bearer {medium_token}", "Content-Type": "application/json"}
    user_id = requests.get("https://api.medium.com/v1/me", headers=headers).json()["data"]["id"]
    data = {
        "title": title,
        "contentFormat": "markdown",
        "content": content,
        "tags": ["engineering", "career", "internships"],
        "publishStatus": "public"
    }
    return requests.post(f"https://api.medium.com/v1/users/{user_id}/posts", json=data, headers=headers).json()

st.title("📡 Engineers Connect Auto Medium Poster")

if st.button("Run: Generate & Publish"):
    topic = random.choice(topics)
    st.write(f"🎯 Topic: **{topic}**")
    with st.spinner("Writing and publishing..."):
        post = generate_post(topic)
        result = post_to_medium(topic, post)
    if "data" in result:
        st.success("✅ Post published!")
        st.markdown(f"[📄 View Post]({result['data']['url']})")
    else:
        st.error("❌ Failed to publish")
        st.json(result)
