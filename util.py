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

  # We can't use the 4096 context length models until we refactor the prompting to only feed a few paragraphs at a time
  completion = openai.ChatCompletion.create(
      # model="gpt-3.5-turbo",
      # model="gpt-3.5-turbo-16k",
      # model="gpt-3.5-turbo-0613",
      model="gpt-3.5-turbo-16k-0613",
      # model="gpt-4",
      # model="gpt-4-32k",
      # model="gpt-4-0613",
      # model="gpt-4-32k-0613",
      messages=chat_context,
      pl_tags=[tag]
  )

  return completion.choices[0].message['content'], chat_context
