from dotenv import load_dotenv
from google import genai


load_dotenv()
client = genai.Client()
first_call = client.interactions.create(
    model='gemini-3.5-flash-lite',
    input="What is AI integrated system? explain one sentence!",
)

print("First call: " + first_call.output_text + "\n\n")
second_call = client.interactions.create(
    model='gemini-3.5-flash-lite',
    input="How to implement it to my web-site, like chat?",
    previous_interaction_id=first_call.id,
)
print("Second call: " + second_call.output_text + "\n\n")


third_call = client.interactions.create(
    model='gemini-3.5-flash-lite',
    input="Summarize, my first and second call!",
    previous_interaction_id=second_call.id,
)

print("Last call: " + third_call.output_text)



