from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os

# Set your Computer Vision subscription key and endpoint
subscription_key = os.getenv('AZURE_CV_KEY')
endpoint = os.getenv('AZURE_CV_ENDPOINT')

# Initialize the Computer Vision client
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Example Blob Storage URL with SAS token
blob_storage_url = os.getenv('blob_storage_url')
sas_token = os.getenv('blob_storage_sas_token')
image_url_with_sas = f"{blob_storage_url}?{sas_token}"

# Use the Computer Vision client to analyze the image
analysis = computervision_client.analyze_image(image_url_with_sas, visual_features=["Description", "Categories", "Tags", "Objects"])

# Print the results
print("Description:")
for caption in analysis.description.captions:
    print(f"'{caption.text}' with confidence {caption.confidence * 100:.2f}%")

print("\nCategories:")
for category in analysis.categories:
    print(f"{category.name} with confidence {category.score * 100:.2f}%")

print("\nTags:")
for tag in analysis.tags:
    print(f"{tag.name} with confidence {tag.confidence * 100:.2f}%")

