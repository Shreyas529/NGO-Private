image_prompt="""Describe the image with distinct items that can be donated. \n\n Ignore people or animals in the image."""

text_prompt="""Identify objects or items in this text that can be donated. \n\n Text: {text} \n\n. Do not give a description. Just the objects that can be donated.Return the output in the format: [object1, object2, object3]"""

categorise_prompt="""Categorise the given objects into the given categories.\n\nReturn the output in the format: [category1, category2, category3].\n\n Input: \n\n Categories: {categories} \n\n Objects: {objects}"""