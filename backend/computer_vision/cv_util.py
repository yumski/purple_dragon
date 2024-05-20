import requests
import os

def ingredients_from_image(image_name):
    # URL for the DETR model
    DETR_API_URL = os.getenv('DETR_API_URL')
    API_TOKEN = os.getenv('CV_API_TOKEN')

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    image_url = f + os.getenv('CV_IMAGE_URL')

    payload = {
        "inputs": {
            "image": image_url
        }
    }

    response = requests.post(DETR_API_URL, headers=headers, json=payload)

    detections = response.json()

    objects = []
    for detection in detections:
        if "label" in detection:
            objects.append(detection['label'])

    NER_API_URL = os.getenv('CV_NER_API_URL')

    text = " ".join(objects)  

    # Prepare the payload
    payload = {
        "inputs": text
    }

    # Make the API request
    try:
        response = requests.post(NER_API_URL, headers=headers, json=payload)
        response.raise_for_status() 
        results = response.json()
    except Exception as e:
        print(f"Error calling the Model: {e}")
        
    # Filter and print food-related words
    food_entities = [result['word'] for result in results if result['entity_group'] == 'FOOD']
    return [food.split(' ') for food in food_entities]

if __name__ == "__main__":
    print(ingredients_from_image("food.jpg"))