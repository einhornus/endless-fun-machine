import os
import glob
import random
import llm

item = "funny image"
trait = "funny"
model = "anthropic/claude-3.7-sonnet:thinking"
#model = "gpt-4.5-preview"


def collect_ideas():
    data_folder = "data"
    txt_files = glob.glob(os.path.join(data_folder, "*.txt"))
    ideas = []
    for file_path in txt_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            ideas.append(content)
    return ideas


def ideate(n=10):
    ideas = collect_ideas()
    random_ideas = random.sample(ideas, n)
    user_message = f"Here are some {item} ideas:\n"
    for index, idea in enumerate(random_ideas):
        user_message += f"{index + 1}. {idea}\n"

    prompt = [
        {
            "role": "user",
            "content": user_message
        },
        {
            "role": "system",
            "content": "You are an exceptionally creative person. \n" +
                       f"Come up with a unique {item} idea in the style of ideas provided.\n" +
                       "Use the ideas provided as a source of inspiration but don't copy them.\n" +
                       "Take your time, think outside the box, and be as creative as possible.\n" +
                       f"The idea must be as {trait} as possible.\n" +
                       f"First, describe clearly what is {trait} about your idea, then write it down.\n" +
                       "Write only the idea, nothing else."
        }
    ]
    idea = llm.call_llm(prompt, model, 0.0)
    return idea


if __name__ == "__main__":
    random.seed(40)
    ideate(10)
