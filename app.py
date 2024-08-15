# Importing necessary libraries
import os
import streamlit as st
from streamlit_option_menu import option_menu
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from utils import load_config

# Set up the Streamlit interface
st.set_page_config(page_title="Prompt Generation Guide", page_icon="📑",layout="wide",initial_sidebar_state="expanded")

# Load environment variables from a .env file
load_dotenv()

# Retrieve the GROQ_API_KEY from the environment variables
groq_api_key = os.getenv('GROQ_API_KEY')

# If the GROQ_API_KEY is not set, display an error message and stop the app
if not groq_api_key:
    st.error("GROQ_API_KEY not found. Please set it in the .env file.")
    st.stop()

# Load additional configuration settings from a config file
config = load_config()

# Dropdown options
image_types = ["None", "Portrait", "Landscape", "Abstract", "Surreal", "Macro", "Conceptual", "Architectural", "Fashion", "Still Life", "Sports", "Nature Close-Up", "Documentary", "Fantasy", "Sci-Fi", "Historical", "Editorial", "Experimental", "Architectural Detail", "Event"]

image_styles = ["None", "Photorealistic", "Cartoon", "Vintage", "Minimalist", "Impressionist", "Abstract Expressionist", "Surrealist", "Art Deco", "Cubist", "Gothic Revival", "Retro", "Expressionist", "Geometric", "Pop Art", "Modernist", "Digital Art", "Hyper-Realistic", "Low Poly", "Pencil Sketch", "Watercolor", "Ink"]

attributes = ["None", "High Contrast", "Soft Focus", "Vivid Colors", "Monochrome", "Sepia Tone", "High Dynamic Range (HDR)", "Low Saturation", "Warm Tones", "Cool Tones", "Grainy", "Muted Colors", "Neon", "Pastel", "Soft Light", "Sharp Detail", "Saturated", "Overexposed", "Underexposed", "Vintage"]

environments = ["None", "Urban", "Nature", "Studio", "Underwater", "Outer Space", "Desert", "Forest", "Beach", "Mountain", "Futuristic City", "Countryside", "Industrial", "Historical", "Fantasy World", "Alien Landscape", "Suburban", "Rural", "Underworld", "Arctic"]

styles_influences = ["None", "Renaissance", "Pop Art", "Futuristic", "Gothic", "Art Nouveau", "Baroque", "Post-Impressionist", "Neo-Classicism", "Digital Art", "Modernist", "Classical", "Abstract", "Avant-Garde", "Constructivism", "Dada", "Rococo", "Symbolist", "Fauvism", "De Stijl"]

moods_emotions = ["None", "Happy", "Sad", "Mystical", "Dramatic", "Serene", "Eerie", "Energetic", "Romantic", "Tense", "Melancholic", "Triumphant", "Whimsical", "Nostalgic", "Mysterious", "Playful", "Somber", "Reflective", "Intense", "Euphoric"]

camera_viewpoints = ["None", "Close-Up", "Wide Angle", "Bird's Eye", "Worm's Eye", "Over-the-Shoulder", "Dutch Angle", "Point of View (POV)", "Overhead", "Eye Level", "Tilted", "Fish Eye", "Panoramic", "High Angle", "Low Angle", "Extreme Close-Up", "Distant"]

camera_types = ["None", "DSLR", "Smartphone", "Film Camera", "Drone", "Medium Format", "Action Camera", "Polaroid", "360-Degree Camera", "Film SLR", "Webcam", "Infrared Camera", "Underwater Camera", "Instant Camera", "Camcorder", "Virtual Reality Camera", "Stereo Camera"]

additional_rendering = ["None", "HDR", "Motion Blur", "Bokeh", "Tilt-Shift", "Soft Glow", "Lens Flare", "Depth of Field", "Color Grading", "Cross-Processing", "Vignette", "Halftone", "Chromatic Aberration", "Duotone", "Glitch Effect", "Film Grain", "Reflections", "Shadows", "Highlight Boost", "Texture Overlay"]

prompt_type = ["None", "Simple", "Creative"]

# Sidebar with navigation
with st.sidebar:
    selected = option_menu("Prompt Generation Guide", ["Image Generation Prompt", "Video Generation Prompt"],
                           icons=['image', 'film'],
                           menu_icon="cast", default_index=0)

# Function to generate the prompt text based on the selected options
def generate_image_prompt(subject, image_type, image_style, attribute, environment, style_influence, mood_emotion, viewpoint, camera_type, rendering_detail, prompt_type):
    prompt_text = f"Create an image of {subject}, depicted as a {image_type} in {image_style} style, showcasing {attribute} attributes. Set the scene in a {environment} environment, influenced by {style_influence} and conveying a {mood_emotion} mood. Capture the scene from a {viewpoint} perspective using a {camera_type}, and render it with {rendering_detail}. Combine all and give me a single {prompt_type} prompt."

    prompt = ChatPromptTemplate.from_messages([("system", prompt_text)])
    model = ChatGroq(
            groq_api_key=groq_api_key,
            model_name=config['model']['model_name'],
            temperature=config['model']['temperature'])
    chain = prompt | model | StrOutputParser()
    return chain.invoke({})

# Function to generate a negative prompt based on the provided prompt text
def generate_negative_prompt(prompt_text):
    prompt_text = f"Generate a negative image generation prompt based on the following prompt: '{prompt_text}'"

    prompt = ChatPromptTemplate.from_messages([("system", prompt_text)])
    model = ChatGroq(
            groq_api_key=groq_api_key,
            model_name=config['model']['model_name'],
            temperature=config['model']['temperature'])
    chain = prompt | model | StrOutputParser()
    return chain.invoke({})

# Function to generate the prompt text based on the selected options
def generate_video_prompt(subject, video_type, video_style, attribute, environment, style_influence, mood_emotion, viewpoint, camera_type, rendering_detail, prompt_type):
    prompt_text = f"Create a captivating video featuring {subject}, presented as a {video_type} in the {video_style} style. Highlight the {attribute} aspects of the subject within a {environment} setting. Draw inspiration from {style_influence} and evoke a {mood_emotion} atmosphere. Frame the scene from a {viewpoint} perspective using a {camera_type}, and ensure the rendering detail is set to {rendering_detail}. Combine all and give me a single {prompt_type} prompt."

    prompt = ChatPromptTemplate.from_messages([("system", prompt_text)])
    model = ChatGroq(
            groq_api_key=groq_api_key,
            model_name=config['model']['model_name'],
            temperature=config['model']['temperature'])
    chain = prompt | model | StrOutputParser()
    return chain.invoke({})

# Image Generation Prompt
if selected == "Image Generation Prompt":
    st.image("img.jpeg")

    # User inputs for image prompt generation
    subject = st.text_input("Description of the Subject")
    
    col1, col2 = st.columns(2)
    
    with col1:
        image_type = st.selectbox("Type of Image", image_types)
        image_style = st.selectbox("Image Style", image_styles)
        attribute = st.selectbox("Attributes/Details", attributes)
        environment = st.selectbox("Environment/Background", environments)
        style_influence = st.selectbox("Style/Artistic Influence", styles_influences)
    
    with col2:
        mood_emotion = st.selectbox("Mood/Emotion", moods_emotions)
        viewpoint = st.selectbox("Camera Viewpoint", camera_viewpoints)
        camera_type = st.selectbox("Camera Type", camera_types)
        rendering_detail = st.selectbox("Additional Rendering Details", additional_rendering)
        prompt_type = st.selectbox("Prompt Type", prompt_type)
    
    # Negative prompt option
    negative_prompt = st.checkbox("Negative Prompt")

    if st.button("Generate Image Prompt"):
        prompt_text = generate_image_prompt(subject, image_type, image_style, attribute, environment, style_influence, mood_emotion, viewpoint, camera_type, rendering_detail, prompt_type)
        st.subheader("Image Generation Prompt")
        st.write(prompt_text)

        if negative_prompt:
            st.subheader("Negative - Image Generation Prompt")
            negative_prompt_text = generate_negative_prompt(prompt_text)
            st.write(negative_prompt_text)

# Video Generation Prompt
elif selected == "Video Generation Prompt":
    st.image("video.jpeg")

    # User inputs for video prompt generation
    subject = st.text_input("Description of the Subject")
    
    col1, col2 = st.columns(2)
    
    with col1:
        video_type = st.selectbox("Type of Video", image_types)
        video_style = st.selectbox("Video Style", image_styles)
        attribute = st.selectbox("Attributes/Details", attributes)
        environment = st.selectbox("Environment/Background", environments)
        style_influence = st.selectbox("Style/Artistic Influence", styles_influences)
    
    with col2:
        mood_emotion = st.selectbox("Mood/Emotion", moods_emotions)
        viewpoint = st.selectbox("Camera Viewpoint", camera_viewpoints)
        camera_type = st.selectbox("Camera Type", camera_types)
        rendering_detail = st.selectbox("Additional Rendering Details", additional_rendering)
        prompt_type = st.selectbox("Prompt Type", prompt_type)

    if st.button("Generate Video Prompt"):
        prompt_text = generate_video_prompt(subject, video_type, video_style, attribute, environment, style_influence, mood_emotion, viewpoint, camera_type, rendering_detail, prompt_type)
        st.subheader("Generated Prompt")
        st.write(prompt_text)