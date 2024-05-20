import pymongo
from pymongo import MongoClient
from bson import ObjectId
import requests
import re
import os

class DBClient :
    
    def __init__(self, collection_name):
        MONGO_URI = os.env('MONGO_URI')
        cluster = MongoClient(MONGO_URI)
        db = cluster["recipemanager"]
        self.collection = db[collection_name]
        
    def insert_document(self, document):
        try:
            document['_id'] = ObjectId()

            self.collection.insert_one(document)
        except Exception as e:
            print(f"Error uploading to DB: {e}")

    def get_user(self, email):
        """
        used for login endpoint
        """
        try:
            user = self.collection.find_one({"email": email})
            return user
        except Exception as e:
            print(f"Error getting user from DB: {e}")

    #TODO AUTHENTICATE CLIENT

    def get_document(self, ingredients):
        try:

            results = self.collection.find({"ingredients": {"$all" : ingredients}})

            recipes = []

            for result in results: 
                recipe["_id"] = str(recipe["_id"]) 
                recipes.append(result)
            
            if not recipes:
                new_recipes = self.generate_recipe(ingredients)

            for recipe in new_recipes:
                self.insert_document(recipe)
                recipe["_id"] = str(recipe["_id"])
                recipes.append(recipe)

            return recipes
        except Exception as e:
            print(f"Error querying the DB: {e}")

    def generate_recipe(self, ingredients):
            # Hugging face model integration
            self.API_URL = os.env('RECIPE_GENERATION_URI')
            self.API_TOKEN = os.env('RECIPE_GENERATION_TOKEN')

            generation_kwargs = {
                "max_length": 512,
                "min_length": 64,
                "no_repeat_ngram_size": 3,
                "do_sample": True,
                "top_k": 60,
                "top_p": 0.95
            }

            inputs = ingredients if isinstance(ingredients, list) else [ingredients]

            # Hugging Face API request
            payload = {
                "inputs": inputs,
                "parameters": generation_kwargs
            }

            headers = {
                "Authorization": f"Bearer {self.API_TOKEN}",
                "Content-Type": "application/json"
            }

            # Make the API request
            response = requests.post(self.API_URL, headers=headers, json=payload)
            response_data = response.json()

            generated_recipes = [item['generated_text'] for item in response_data]

            recipes_dicts = []

            pattern_ingredients = r'(?=\d)'

            pattern_directions = re.compile(r"(?<!\blb)(?<!\boz)(?<!\bsp)\. ")
            
            # split sections
            for text in generated_recipes:
                recipe = {}
                recipe["title"] = text[text.find("title:")+len("title:"):text.rfind("ingredients:")].strip()
                ingredients_list = text[text.find("ingredients:")+len("ingredients:"):text.rfind("directions:")].strip()
                ingredients_list = re.split(pattern_ingredients, ingredients_list)

                ingredients_formatted = []
                i = 0
                while i < len(ingredients_list):
                    # Check if the current part is a number or numbers separated by spaces
                    if re.match(r'^\d+(\s\d+)*$', ingredients_list[i].strip()):
                        # Join it with the next part
                        if i + 1 < len(ingredients_list):
                            ingredients_formatted.append(ingredients_list[i] + ingredients_list[i + 1])
                            i += 2
                        else:
                            ingredients_formatted.append(ingredients_list[i])
                            i += 1
                    else:
                        ingredients_formatted.append(ingredients_list[i])
                        i += 1

                recipe["ingredients"] = [item.strip() for item in ingredients_formatted if item]

                directions = text[text.find("directions:")+len("directions:"):].strip()
                directions = re.split(pattern_directions, directions)
                recipe["directions"] = [item.strip() for item in directions if item]
                recipes_dicts.append(recipe)
            
            '''pattern = re.compile(r"(?<!\blb)(?<!\boz)(?<!\bsp)\. ")
            
            # split sections
            for text in generated_recipes:
                recipe = {}
                words = text.split(' ')
                key = None
                section = []

                for word in words:
                    if ':' in word:
                        if key:
                            recipe[key] = ' '.join(section).strip()
                            if key in ["ingredients", "directions"]:
                                val = []
                                for s in pattern.split(recipe[key]):
                                    if len(s) != 0:
                                        val.append(s)
                                recipe[key] = val
                                
                        key, val = word.split(':', 1)
                        section = [val]
                    else:
                        section.append(word)
            
                if key:
                    recipe[key] = ' '.join(section).strip().split(". ")
            
                recipes_dicts.append(recipe)'''

            return recipes_dicts



if __name__ == "__main__":
    dbClient = DBClient("recipe")
    print(dbClient.generate_recipe(["flour"]))
    # recipe = {"name": "Pancakes", "ingredients": ["flour", "milk", "eggs", "sugar", "butter"]}
    # dbClient.insert_document(recipe)
    results = dbClient.get_document(["chili"])
    print(results)