import openai
import os
from dotenv import load_dotenv
import re
from flask import Flask, render_template, request

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def generate_mind_map(topic):
    prompt = f"""
    Generate a comprehensive wiki-style mind map for "{topic}". The mind map should adhere to the following markdown guidelines:
    1. Start with the topic as the central idea and use # to denote the main topic in 5 words or less if necessary.
    2. Break down the topic into its main categories, themes or pillars. Use ## at the start of the line for each main category.
    3. Further break down each main category into subcategories, key points or supporting details. Use ###,####,#####,###### respectively at the start of the line for each subcategory.
    4. Add and split out relevant details, examples, facts or explanations under each subcategory. Use a hyphen (-) at the start of the line for each point.
    5. Aim to comprehensively cover the essential aspects of the topic concisely. The mind map should break down the subject into a clear hierarchy of ideas.
    6. Structure the mind map to enable an exploratory learning approach. Users should be able to navigate the main categories and discover key information about the different facets of the topic.
    Please use the specified Markdown formatting (#, ##, ###,####,#####,###### -) to format the mind map content for clarity and readability without any begininng or ending commentary
    """
    response = openai.ChatCompletion.create(
        model="gpt-4-0125-preview",  # Use the correct and most up-to-date model
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates Markdown-formatted mind maps."},
            {"role": "user", "content": prompt}
        ]
    )
    mind_map_markdown = response.choices[0].message.content
    return mind_map_markdown

def generate_file_name(topic, max_length=25):
    file_name = re.sub(r'[^a-zA-Z0-9\s]', '', topic)
    file_name = file_name.replace(' ', '_')
    if len(file_name) > max_length:
        file_name = file_name[:max_length]
    return file_name

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        topic = request.form['topic']
        mind_map = generate_mind_map(topic)
        file_title = generate_file_name(topic)
        return render_template('mind_map.html', file_title=file_title, mind_map=mind_map)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
