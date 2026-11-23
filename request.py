from dotenv import load_dotenv
from google import genai


load_dotenv()
client = genai.Client()

my_requests = ["Меня зовут Ернур!", "Столица Казахстана?", "Что такое регламент?", "Как меня зовут?"]
roles = ["Ты строгий ИИ", "Ты учитель Историй", "ТЫ политик", "Ты не разговорчивый ИИ"]
a = 0
while a<len(my_requests):
    call = client.interactions.create(
        model='gemini-3.5-flash-lite',
        input=my_requests[a],
        system_instruction=roles[a],
    )
    usage = call.usage.total_tokens
    print("Answer: " + call.output_text + "\nUsage: " + usage)
    a+=1




# first_call = client.interactions.create(
#     model='gemini-3.5-flash-lite',
#     input="What is AI integrated system? explain one sentence!",
# )

# print("First call: " + first_call.output_text + "\n\n")
# second_call = client.interactions.create(
#     model='gemini-3.5-flash-lite',
#     input="How to implement it to my web-site, like chat?",
#     previous_interaction_id=first_call.id,
# )
# print("Second call: " + second_call.output_text + "\n\n")


# third_call = client.interactions.create(
#     model='gemini-3.5-flash-lite',
#     input="Summarize, my first and second call!",
#     previous_interaction_id=second_call.id,
# )

# print("Last call: " + third_call.output_text)



