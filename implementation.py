import models

# implementation_model = "anthropic/claude-3.7-sonnet:thinking"
implementation_model = "gpt-4.1"


def implement_idea(idea):
    prompt = [
        {
            "role": "system",
            "content": "You are an exceptionally talented visual designer.\n" +
                       "You are given an idea for a funny picture.\n" +
                       "Visualize this idea, provide an image description.\n" +
                       "Focus on what makes it funny. Avoid excessive text\n" +
                       "Please be concise and straight to the point.\n" +
                       "Write only the image description, nothing else."
        },
        {
            "role": "user",
            "content": f"Here's a funny idea:\n\n```{idea}```\n\nWrite an image description."
        },
    ]
    detailed_description = models.call_llm(prompt, implementation_model, 0)
    return detailed_description


if __name__ == "__main__":
    sample_idea = "A penguin trying to hail a taxi in New York City"
    detailed_description = implement_idea(sample_idea)
    print("\nDETAILED IMAGE DESCRIPTION:")
    print("--------------------------")
    print(detailed_description)
