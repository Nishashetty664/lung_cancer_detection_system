import gradio as gr
import cv2
import numpy as np
from skimage.feature import hog
from joblib import load
import pandas as pd

# Load the trained models and scaler
svm_model = load('svm_model.joblib')
scaler = load('scaler.joblib')
rf_model = load('random_forest_model.pkl')

# Parameters for preprocessing
image_size = (128, 128)
orientations = 9
pixels_per_cell = (8, 8)
cells_per_block = (2, 2)

# Preprocessing and feature extraction function for images
def preprocess_image(image):
    image_resized = cv2.resize(image, image_size)
    gray_image = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
    normalized_image = gray_image / 255.0
    hog_features = hog(
        normalized_image,
        orientations=orientations,
        pixels_per_cell=pixels_per_cell,
        cells_per_block=cells_per_block,
        block_norm='L2-Hys',
        visualize=False
    )
    return hog_features

# Classification function for images
def classify_image(image):
    if image is None:
        return "Please upload an image."
    
    if not is_lung_image(image):
        return "Please provide a valid lung image."
    
    hog_features = preprocess_image(image)
    hog_features_scaled = scaler.transform([hog_features])
    prediction = svm_model.predict(hog_features_scaled)
    return f"Prediction: {prediction[0]}"

# Simple function to check if the uploaded image might represent a lung image
def is_lung_image(image):
    return True  # Placeholder logic

# Classification function for patient history
def classify_patient_history(age, gender, shortness_of_breath, allergy, fatigue, swallowing_difficulty, anxiety, yellow_fingers, chronic_disease, smoking, alcohol_consuming, wheezing, peer_pressure, cough, chest_pain):
    if age is None:
        return "Please provide an age."
    if not gender:
        return "Please select a gender."
    if not any([shortness_of_breath, allergy, fatigue, swallowing_difficulty, anxiety, yellow_fingers, chronic_disease, smoking, alcohol_consuming, wheezing, peer_pressure, cough, chest_pain]):
        return "Please select at least one symptom."
    
    gender_encoded = 1 if gender == 'Male' else 0
    input_data = pd.DataFrame({
        'GENDER': [gender_encoded],
        'AGE': [age],
        'SMOKING': [1 if smoking else 0],
        'YELLOW_FINGERS': [1 if yellow_fingers else 0],
        'ANXIETY': [1 if anxiety else 0],
        'PEER_PRESSURE': [1 if peer_pressure else 0],
        'CHRONIC_DISEASE': [1 if chronic_disease else 0],
        'FATIGUE': [1 if fatigue else 0],
        'ALLERGY': [1 if allergy else 0],
        'WHEEZING': [1 if wheezing else 0],
        'ALCOHOL_CONSUMING': [1 if alcohol_consuming else 0],
        'COUGHING': [1 if cough else 0],
        'SHORTNESS_OF_BREATH': [1 if shortness_of_breath else 0],
        'SWALLOWING_DIFFICULTY': [1 if swallowing_difficulty else 0],
        'CHEST_PAIN': [1 if chest_pain else 0]
    })

    input_data = input_data[rf_model.feature_names_in_]
    prediction = rf_model.predict(input_data)

    return "Cancer detected: Yes" if prediction[0] == 1 else "Cancer detected: No"

# Gradio interface for image classification
image_interface = gr.Interface(
    fn=classify_image,
    inputs=gr.Image(type="numpy", label="Upload Image"),
    outputs=gr.Textbox(label="Prediction"),
    live=False,
    title="Image Classifier with SVM",
    description="Upload a lung image to get the predicted label using a trained SVM model."
)

# Gradio interface for patient history input
history_interface = gr.Interface(
    fn=classify_patient_history,
    inputs=[
        gr.Slider(label="Age", minimum=0, maximum=100, step=1),
        gr.Radio(label="Gender", choices=["Male", "Female"]),
        gr.Checkbox(label="Shortness of Breath"),
        gr.Checkbox(label="Allergy"),
        gr.Checkbox(label="Fatigue"),
        gr.Checkbox(label="Swallowing Difficulty"),
        gr.Checkbox(label="Chest Pain"),
        gr.Checkbox(label="Anxiety"),
        gr.Checkbox(label="Yellow Fingers"),
        gr.Checkbox(label="Chronic Disease"),
        gr.Checkbox(label="Smoking"),
        gr.Checkbox(label="Alcohol Consuming"),
        gr.Checkbox(label="Wheezing"),
        gr.Checkbox(label="Peer Pressure"),
        gr.Checkbox(label="Cough")
    ],
    outputs=gr.Textbox(label="Prediction"),
    live=False,
    title="Patient History Classifier",
    description="Unlock the power of AI for lung health! Enter patient history details to reveal insightful predictions with our advanced Random Forest model."
)

# Add a custom header with logo and title
header = """
<div style="text-align: center; margin-bottom: 20px;">
    
    <h1 style="font-family: Arial, sans-serif; color: #4CAF50; margin: 10px;">Lung Vision AI</h1>
</div>
"""

# Combine interfaces into tabs
iface = gr.TabbedInterface(
    [image_interface, history_interface],
    ["Lung Image Classification", "Patient History Classification"],
    theme="compact"
)

# Add header above the tabs
app = gr.Blocks()
with app:
    gr.HTML(header)
    iface.render()

# Launch the interface
app.launch()
