import llm


def implement_idea(idea, trait="funny", model="anthropic/claude-3.7-sonnet"):
    prompt = [
        {
            "role": "system",
            "content": "You are an exceptionally creative visual designer and storyteller.\n" +
                       f"Transform the given idea into {trait} image description.\n" +
                       "Think through the art style and the implementation\n" +
                       "Please be concise and straight to the point.\n" +
                       "Write only the image description, nothing else."
        },
        {
            "role": "user",
            "content": f"Here's {trait} image idea:\n\n{idea}\n\nExpand this into a detailed image description."
        },
    ]
    detailed_description = llm.call_llm(prompt, model, 0)
    return detailed_description


if __name__ == "__main__":
    sample_idea = "A penguin trying to hail a taxi in New York City"
    detailed_description = implement_idea(sample_idea, trait="funny")
    print("\nDETAILED IMAGE DESCRIPTION:")
    print("--------------------------")
    print(detailed_description)
