# Endless Fun Machine
AI coming up with funny pics ideas and generating them using OpenAI gpt-image-1

## How to use

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Rename keys.template.json to keys.json and add your API keys. OpenAI key is always required. Open Router key is only required if you want to use OpenRouter models.
3. Verify your organization on the OpenAI API Platform

4. Run main.py. The results will be saved in the `results` folder.


## Configuration
1. describing.py: 
   - model is the LLM which is used to describe the image in the reference set. Must be able to receive images.
2. ideation.py:
   - ideation_model is the LLM which is used to generate ideas
   - n_references is the number of references from the reference set the ideation model is inspired by
   - temperature is the temperature for the ideation model
   - estimation_model is the LLM which is used to estimate ideas
   - n_ideas is the number of ideas to estimate and choose from
3. implementation.py
   - implementation_model is the LLM used to write the image prompt for OpenAI gpt-image-1