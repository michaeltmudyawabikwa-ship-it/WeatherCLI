import requests
import json

name = input("Enter a name: ")

try:
    response = requests.get(f"https://api.agify.io?name={name}")
    response.raise_for_status()
    data = response.json()

    with open('age_data.json','w') as f:
        json.dump(data, f, indent=4)


    print(f"Name: {data['name']}")
    print(f"Predicted Age : {data['age']}")
    print("Saved to age_data.json ")  

except:
    print("Ooops! Check your internet or try another name")  
