import asyncio
import base64
import aiohttp
import aiofiles
from openai import AsyncOpenAI

from config import AI_API_TOKEN

client = AsyncOpenAI(api_key=AI_API_TOKEN)


async def gpt_text(req, model):
    """Text generation"""
    completion = await client.chat.completions.create(
        messages=[{'role': 'user', 'content': req}],
        model=model
    )
    return {'response': completion.choices[0].message.content,
            'usage': completion.usage.total_tokens}


async def gpt_image(req, model):
    """Image generation"""
    response = await client.images.generate(
        model='dall-e-3',
        prompt=req,
        size='1024x1024',
        quality='standard',
        n=1,
    )
    return {'response': response.data[0].url,
            'usage': 1}


async def encode_image(image_path):
    """Function to encode the image"""
    async with aiofiles.open(image_path, 'rb') as image_file:
        return base64.b64encode(await image_file.read()).decode('utf-8')


async def gpt_vision(req, model, file):
    base64_image = await encode_image(file)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {AI_API_TOKEN}'
    }

    payload = {
        'model': model,
        'messages': [
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'image_url',
                        'image_url': {
                            'url': f'data:image/jpeg;base64,{base64_image}'
                        }
                    }
                ]
            }
        ],
        'max_tokens': 300
    }

    if req is not None:
        payload['messages'][0]['content'].append({
            'type': 'text',
            'text': req
            })

    async with aiohttp.ClientSession() as session:
        async with session.post('https://api.openai.com/v1/chat/completions', headers=headers, json=payload) as response:
            completion = await response.json()
            print(completion)
    return {'response': completion['choices'][0]['message']['content'],
            'usage': completion['usage']['total_tokens']}
