import time

from ultralytics import YOLO
from matplotlib import pyplot as plt
from PIL import Image
import requests
from io import BytesIO

model = YOLO('yolov8n.pt')

url1 = "https://media.wbur.org/wp/2016/06/0629_interstate-traffic-getty-1000x673.jpg"
url2 = "https://cdn.thewirecutter.com/wp-content/media/2023/06/laptops-2048px-5607.jpg?auto=webp&quality=75&crop=1.91:1&width=1200"
url3 = "https://hips.hearstapps.com/hmg-prod/images/bethany-adams-interiors-j-l-jordan-photography-657c85285a3a4.jpg"

response = requests.get(url1)
img = Image.open(BytesIO(response.content))

results = model(source=img)
results[0].show()

response = requests.get(url2)
img = Image.open(BytesIO(response.content))

results = model(source=img, save=True)
results[0].show()

response = requests.get(url3)
img = Image.open(BytesIO(response.content))

results = model(source=img ,save=True)
results[0].show()
