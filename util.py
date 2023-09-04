import os
# import openai
import promptlayer

promptlayer.api_key = os.getenv("PROMPTLAYER_API_KEY", "pl_07c539f21ce8774c65e271a4c87d9da5")
openai = promptlayer.openai
openai.api_key = os.getenv("OPENAI_API_KEY", "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")

def read_file_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def replace_text(template_string, placeholder, replacement):
    return template_string.replace(placeholder, replacement)

async def send_openai_message(prompt, template, tag, existing_context=None):
  chat_context = [
    {"role": "system", "content": prompt},
    {"role": "user", "content": template}
  ]

  if existing_context:
     chat_context = existing_context + chat_context

  completion = openai.ChatCompletion.create(
      model="gpt-4",
      messages=chat_context,
      pl_tags=[tag]
  )

  return completion.choices[0].message['content'], chat_context
