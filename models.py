from openai import OpenAI
import json
import time
import base64
import re
from PIL import Image
import io


def encode_image(image_path):
    with Image.open(image_path) as img:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=95)
        return base64.b64encode(buffer.getvalue()).decode('utf-8')


def parse_text_with_images(text):
    image_pattern = r'<image>(.*?)</image>'
    parts = re.split(image_pattern, text)
    res = []
    for part in parts:
        if part.strip():
            if part.endswith('.jpeg') or part.endswith('.jpg') or part.endswith('.png'):
                res.append({'type': 'image', 'content': part.strip()})
            else:
                res.append({'type': 'text', 'text': part.strip()})
    return res


def transform_message(message):
    parsed_media = parse_text_with_images(message['content'])
    has_media = any(part['type'] in ['image'] for part in parsed_media)

    if not has_media:
        return message

    content_list = []
    for part in parsed_media:
        if part["type"] == "image":
            content_list.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encode_image(part['content'])}",
                },
            })
        else:
            content_list.append(part)

    return {
        "role": message["role"],
        "content": content_list
    }


def get_openai_api_key():
    return json.load(open('keys.json', encoding='utf-8'))["OPEN_AI_API_KEY"]


def get_openrouter_api_key():
    return json.load(open('keys.json', encoding='utf-8'))["OPEN_ROUTER_API_KEY"]


def call_llm(messages, model, temperature=0, max_tokens=1000):
    if "/" in model:
        api_key = get_openrouter_api_key()
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
    else:
        api_key = get_openai_api_key()
        client = OpenAI(
            api_key=api_key
        )

    for i in range(len(messages)):
        messages[i] = transform_message(messages[i])

    for i in range(8):
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            if completion.choices is None:
                continue

            res = completion.choices[0].message.content
            return res
        except Exception as e:
            print(e)
            print(f"Retrying in {2 ** i} seconds...")
            time.sleep(2 ** i)
    return None


def gen_image(prompt, output_file_name):
    api_key = get_openai_api_key()
    client = OpenAI(
        api_key=api_key
    )
    result = client.images.generate(
        model="gpt-image-1",
        size="1024x1536",
        quality="high",
        prompt=prompt
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)
    with open(output_file_name, "wb") as f:
        f.write(image_bytes)
