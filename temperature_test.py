from dotenv import load_dotenv
from google import genai
import time

load_dotenv()
client = genai.Client()

print("Temperature 0: ")

for i in range(5):
    response = client.interactions.create(
        model='gemini-3.5-flash-lite',
        input="Придумай название для кофейни. Напиши только одно!",
        generation_config={
            "temperature": 0
        }
    )
    print(f"[{i}]  Name: " + response.output_text)
    time.sleep(0.5)


print("Temperature 1: ")
time.sleep(1.5)

for i in range(5):
    response = client.interactions.create(
        model='gemini-3.5-flash-lite',
        input="Придумай название для кофейни. Напиши только одно!",
        generation_config={
            "temperature": 1
        }
    )
    print(f"[{i}]  Name: " + response.output_text)
    time.sleep(0.5)




