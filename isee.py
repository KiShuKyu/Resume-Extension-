from PIL import Image 
import pytesseract 
import cv2 as cv
import numpy
from pdf2image import convert_from_path
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# print(numpy.__version__)
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# images = convert_from_path('image\\testocr.pdf', poppler_path=r'C:\poppler\poppler-25.12.0\Library\bin')

# for i, img in enumerate(images):
#     # 3. Extract text from image
#     text = pytesseract.image_to_string(img)
#     print(f"--- Page {i+1} ---")
#     print(text)

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents="What is a syntax error?",

# )
# print(response.text)

# response = client.models.generate_content(
#     model='gemini-2.5-flash',
#     contents='A cartoon infographic for flying sneakers',
#     config=types.GenerateContentConfig(
#         response_modalities=["IMAGE"],
#         image_config=types.ImageConfig(
#             aspect_ratio="9:16",
#         ),
#     ),
# )

# for part in response.parts:
#     if part.inline_data:
#         generated_image = part.as_image()
#         generated_image.show()

uploaded_file = client.files.upload(file='image\\VishalJha.pdf')
# proff=input("For what proffession do you want this resume for?")


prompt = """
Analyze the resume strictly for the role of engineers.

Return the response STRICTLY as valid JSON.
DO NOT add explanations, markdown, or extra text 

JSON format:
{{
  "goodPoints": [
    "Strong project experience",
    "Clear technical skill section",
    "Good formatting"
  ],
  "badPoints": [
    "Too long summary",
    "Missing quantified achievements"
  ],
  "improvements": [
    "Add metrics to project descriptions",
    "Tailor resume keywords to job description"
  ]
  "jdMatch": {
    "score": 72,
    "missingSkills": ["Docker", "AWS"],
    "suggestedKeywords": ["REST API", "CI/CD"]}
}}
"""

respose = client.models.generate_content(
    model='gemini-2.5-flash',
    config=types.GenerateContentConfig(
        system_instruction=prompt # Overall role
    ),
    contents=['Analyze the provided text and give feedback.', uploaded_file]
)

print(respose.text)
client.close()



# # 1. Define a class (the blueprint)
# class Dog:
#     def __init__(self, name, age):
#         """The constructor method to initialize object attributes."""
#         self.name = name  # Instance attribute
#         self.age = age    # Instance attribute

#     def bark(self):
#         """A method that defines the object's behavior."""
#         print(f"{self.name} is barking!")

# # 2. Create objects (instances of the class)
# dog1 = Dog("Buddy", 3)
# dog2 = Dog("Max", 5)

# # 3. Access attributes and call methods
# print(f"Dog 1 name: {dog1.name}, age: {dog1.age}")
# dog1.bark()

# print(f"Dog 2 name: {dog2.name}, age: {dog2.age}")
# dog2.bark()




# img_cv = cv.imread(r'image/testocr.png'
# img_rgb = cv.cvtColor(img_cv, cv.COLOR_BGR2RGB)
# print(pytesseract.image_to_string(img_rgb))

# cv.imshow("Image", img_cv)
# cv.waitKey(0)

#grayscale threshold resizing to help improve images