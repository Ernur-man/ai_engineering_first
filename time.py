from google import genai
from dotenv import load_dotenv
import asyncio
import time
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Optional


load_dotenv()
client = genai.Client()

# по умолчанию если передать не тот тип "20"(хотя нам нужен int) pydantic автоматический преобразует их в int "20" -> 20
# class Pop(BaseModel):
#     model_config = ConfigDict(strict=True)
#     name: str
#     age: int


# class Registration(BaseModel):
#     username: str = Field(min_length=3)
#     password: str = Field(min_length=8, max_length=16)
#     confirm_password: str

#     @field_validator("username")
#     @classmethod
#     def validate_username(cls, value):
#         if " " in value:
#             raise ValueError("User cannot contain spaces")
#         return value

#     @model_validator(mode="after")
#     def validate_password(self):
#         if self.password != self.confirm_password:
#             raise ValueError("They must be match")
#         return self


# class Address(BaseModel):
#     city: str
#     country: str

# class User(BaseModel):
#     username: str
#     email: str
#     address: Address

# class Product(BaseModel):
#     name: str
#     price: float
# class Order(BaseModel):
#     user: User
#     products: list[Product]

# address = Address(
#     city="Astana",
#     country="KZ"
# )
# user = User(
#     username="Yernur",
#     email="ernur@gmail.com",
#     address=address
# )

# product1 = Product(name="Iphone", price=1200.0)
# product2 = Product(name="GTA6", price=100.0)

# order = Order(user=user, products=[product1, product2])

# print(order.model_dump())

# async def calling(message, prompt=""):

#     for i in range(3):
#         attempt_start = time.perf_counter()

#         try:
#             chat = await asyncio.wait_for(
#                 client.aio.interactions.create(
#                     model="gemini-3.5-flash-lite",
#                     input=message,
#                     system_instruction=prompt,
#                 ),
#                 timeout=60.0
#             )
#             print(f"Response: {time.perf_counter() - attempt_start:.2f}s")
#             print(chat.output_text)
#             return chat
#         except asyncio.TimeoutError:
#             print(f"Timeout after {time.perf_counter() - attempt_start:.2f}s")
#             print("Time is out!")
#         except Exception as e:
#             status_code = getattr(e, "status_code", None)
#             retryable = status_code == 429 or (
#                 status_code is not None and 500 <= status_code <= 599
#             )
#             if not retryable:
#                 print(f"API Error (no retry): {e}")
#                 return None
#             print(f"Retryable error {status_code}")


#         if i < 2:
#             await asyncio.sleep(2 ** i)

#     print("All attempts failed!")
#     return None



# start = time.perf_counter()
# asyncio.run(calling("Hello! My name is Yernur, and I am studying at AITU. My major is Computer Science! I would like ask you advice, I am doing 3 things at once, study, work and millitaty! What should you advice to me?", "You are a helpful assistant."))
# end = time.perf_counter()

# print(f"Time: {end-start:.2f}")





messages = [
    "Меня зовут Асель, хочу заказать 2 пары кроссовок Nike в Астану, нужно срочно, к завтрашнему дню.",
    "Здравствуйте, это Данияр. Закажите мне, пожалуйста, 1 ноутбук Lenovo. Доставка в Алматы, не горит.",
    "Айгерим здесь. Нужно 5 футболок с логотипом компании, срочно, доставка в Шымкент.",
    "Меня зовут Тимур, беру три книги по Python. Город не важно, заберу сам.",
    "Бекзат. Одну клавиатуру Logitech, когда будет возможность, отправьте в Караганду.",
    "Привет, подскажите, какой у вас режим работы?"
]

class Order(BaseModel):
    customer_name: str = Field(min_length=3)
    product: str
    quantity: int = Field(gt=0)
    city: Optional[str] = None
    urgent: bool = True


for msg in messages:
    call = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=msg,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": Order.model_json_schema()
        }
    )
    order = Order.model_validate_json(call.output_text)
    print(order.model_dump())
    time.sleep(0.5)


# prompt:
# {'customer_name': 'null', 'product': 'null', 'quantity': 0, 'city': None, 'urgent': False}
# Optional[str] = None
# {'customer_name': None, 'product': None, 'quantity': None, 'city': None, 'urgent': None}
# gt=0:
# Traceback (most recent call last):
#   File "C:\Users\user\Desktop\AI_engineering\fix_environment\time.py", line 147, in <module>
#     order = Order.model_validate_json(call.output_text)
#   File "C:\Users\user\Desktop\AI_engineering\fix_environment\Lib\site-packages\pydantic\main.py", line 847, in model_validate_json
#     return cls.__pydantic_validator__.validate_json(
#            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
#         json_data, strict=strict, extra=extra, context=context, by_alias=by_alias, by_name=by_name
#         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#     )
#     ^
# pydantic_core._pydantic_core.ValidationError: 1 validation error for Order
# quantity
#   Input should be greater than 0 [type=greater_than, input_value=0, input_type=int]
#     For further information visit https://errors.pydantic.dev/2.14/v/greater_than
