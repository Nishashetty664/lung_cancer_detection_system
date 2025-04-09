# 🫁 Lung Cancer Detection System
## 📌 Overview
Lung Cancer Detection System is a smart diagnostic tool that:

📷 Classifies CT scan images into Benign, Malignant, or Normal categories

🧑‍⚕️ Analyzes patient history to predict the presence of lung cancer

Designed to reduce human error and assist in early, accurate diagnosis.

## 🎯 Objectives
✅ Automate lung cancer detection using CT scan images

✅ Predict cancer risk based on structured patient history

✅ Increase accuracy, consistency, and accessibility in medical diagnostics

## 🛠️ Technologies Used
Library         	Version

Python          	3.11.9

pandas	          2.2.3

numpy	            2.1.3

OpenCV          	4.10.0.84

scikit-image     	0.24.0

scikit-learn    	1.5.2

matplotlib	      3.9.2

seaborn	          0.11.2

tqdm	            4.67.0

joblib          	1.4.2

Gradio	        

## 🧠 ML Models Used
### 🔍 Image Classification:

HOG (Histogram of Oriented Gradients) for feature extraction

SVM: Achieved 99.09% accuracy

KNN: 94.55%

Random Forest: 91.82%

### 🧾 Patient History Classifier:

Random Forest trained on a structured dataset with 3000 rows and 16 features

Accuracy optimized with:

IQR-based outlier removal

Label Encoding

Standard Scaler for feature normalization

## 🖥️ System Features
### 1. 🖼️ Lung Image Classifier
Upload a CT scan image

The system classifies it as:

Benign

Malignant

Normal


### 2. 📋 Patient History Predictor
Input fields: Age, Gender, Symptoms (fatigue, smoking, coughing, etc.)

Model predicts cancer presence based on clinical data

## 🧪 Final Interface

![Screenshot (82)](https://github.com/user-attachments/assets/15c36951-6e91-4ba2-b4f9-b204ff71d468)

![image](https://github.com/user-attachments/assets/c823af74-275b-4ff6-9724-4edfc417a424)


## 🔮 Future Enhancements
🔁 Integrate deep learning (e.g., CNNs) for more robust image recognition

☁️ Deploy as a web-based solution for hospital and clinical use

