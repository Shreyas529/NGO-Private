


from groq import Groq
import base64
from AI.prompts import image_prompt, text_prompt, categorise_prompt
from dotenv import load_dotenv
load_dotenv()


class Response:
    def __init__(self, type:str, content):
        self.type=type
        self.content=content
        self.client=Groq()
        if type=="image":
            self.content=self._handle_image()
            self.objects=self._handle_text()
        else:
            self.objects=self._handle_text()

    def _handle_image(self):

        chat_completion = self.client.chat.completions.create(
            messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": image_prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{self.content}",
                        },
                    },
                ],
            }
        ],
        model="llava-v1.5-7b-4096-preview",
    )
        response=chat_completion.choices[0].message.content
    
        return response
    
    def _handle_text(self):

        chat_completion = self.client.chat.completions.create(
            messages=[
            {
                "role": "user",
                "content": 
                  text_prompt.format(text=self.content),
            }
        ],
        model="llama-3.1-70b-versatile")

        response=chat_completion.choices[0].message.content
        response=response[response.find("[")+1:response.find("]")]
        response=response.split(",")
        return response
    
    def _categorise_objects_to_NGO(self,NGO_categories):

        chat_completion = self.client.chat.completions.create(
            messages=[
            {
                "role": "user",
                "content": 
                     categorise_prompt.format(categories=",".join(NGO_categories),objects=",".join(self.objects)),
            }
        ],
        model="llama-3.1-70b-versatile")

        response=chat_completion.choices[0].message.content
        response=response[response.find("[")+1:response.find("]")]
        response=response.split(",")
        return list(set(response))
        


# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
response=Response("image",encode_image("download.jpeg"))
