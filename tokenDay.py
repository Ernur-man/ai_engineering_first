# Second Day


from dotenv import load_dotenv
from google import genai
import time




load_dotenv()
client = genai.Client()


messages = [
    "Заказ уже 10 дней в пути, трек не обновляется.",
    "С карты списали деньги дважды за один заказ",
    "Хочу вернуть куртку, не подошёл размер.",
    "Приложение вылетает при открытии корзины.",
    "Когда курьер привезёт заказ? Жду с утра.",
    "Не могу оплатить заказ: ошибка «Платёж отклонён».",
    "Товар пришёл со сломанной застёжкой, верните деньги.",
    "Не приходит код подтверждения на телефон при входе.",
    "Можно ли оплатить заказ при получении?",
    "Посылку принесли в другой подъезд, не нашёл её."
]

prompts = [
    "Определи, к какой категории относится сообщение клиента: доставка, оплата, возврат или техническая проблема.",
    "Ты классификатор сообщений клиентов. Категории: доставка, оплата, возврат, техническая_проблема. Ответь ровно одним словом из этого списка. Без пояснений, без точки, строчными буквами.",
    """
    Ты классификатор сообщений клиентов.
    Категории: доставка, оплата, возврат, техническая_проблема.
    Ответь ровно одним словом из списка.

    Сообщение: Курьер не звонит, а время доставки прошло.
    Ответ: доставка

    Сообщение: Скиньте реквизиты для безналичной оплаты.
    Ответ: оплата

    Сообщение: Сайт не открывается с телефона.
    Ответ: техническая_проблема
"""
]


# for i, prompt in enumerate(prompts, 1):
#     print(f"\n\n[{i}] call: ")
#     for message in messages:
#         call = client.interactions.create(
#             model="gemini-3.5-flash-lite",
#             input=message,
#             system_instruction=prompt
#         )
#         print("Answer: " + call.output_text)

message = "Объясни, как работает streaming в LLM API. Напиши около 300 слов: что это, чем отличается от обычного запроса, зачем нужен в чат-приложениях."
# start = time.perf_counter()
# first_call = client.interactions.create(
#     model="gemini-3.5-flash-lite",
#     input=message,
#     response_format={"type": "text"},
#     stream=True,
# )

# for event in first_call:
#     if event.event_type == "step.delta":
#         if event.delta.type == "text":
#             print(event.delta.text, end="", flush=True)
# end = time.perf_counter()
# print(f"\n\nFirst call: {end-start:.6f}")

# second_start = time.perf_counter()

# second_call = client.interactions.create(
#     model="gemini-3.5-flash-lite",
#     input=message,
#     response_format={"type": "text"}
# )
# second_end = time.perf_counter()
# print(second_call.output_text)

# print(f"\n\nSecond call: {second_end-second_start:.6f}")

call = client.interactions.create(
    model="gemini-3.5-flash-lite",
    input=message,
)

inputPrice = 0.30
outputPrice = 2.50
cost = (call.usage.total_input_tokens/1000000) * inputPrice + (call.usage.total_output_tokens/1000000) * outputPrice

print(f"Input tokens: {call.usage.total_input_tokens}")
print(f"Output tokens: {call.usage.total_output_tokens}")
print(f"Total cost: ${cost:.8f}")
