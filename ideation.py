import os
import glob
import random
import models
import re

# ideation_model = "anthropic/claude-3.7-sonnet:thinking"
ideation_model = "gpt-4.1"
# estimation_model = "anthropic/claude-3.7-sonnet"
estimation_model = "gpt-4.1"
temperature = 0.0
n_references = 5
n_ideas = 1


def collect_ideas():
    data_folder = "data"
    txt_files = glob.glob(os.path.join(data_folder, "*.txt"))
    ideas = []
    for file_path in txt_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            ideas.append(content)
    return ideas


def come_up_with_idea():
    ideas = collect_ideas()
    random_ideas = random.sample(ideas, n_references)
    user_message = f"Here are some funny image ideas:\n"
    for index, idea in enumerate(random_ideas):
        user_message += f"{index + 1}. {idea}\n"

    prompt = [
        {
            "role": "system",
            "content": "You are an exceptionally creative person.\n" +
                       "Come up with a unique funny idea in the style of ideas provided.\n" +
                       "Use the ideas provided as a source of inspiration but don't copy them.\n" +
                       "Take your time, think outside the box, and be as witty and creative as possible.\n" +
                       "The idea must be as funny as possible.\n" +
                       "Please be concise and straight to the point.\n" +
                       "First, describe clearly what is funny about your idea, then write it down.\n"
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    idea = models.call_llm(prompt, ideation_model, temperature)
    return idea


def ideate():
    if n_ideas == 1:
        return come_up_with_idea()
    ideas = []
    for i in range(n_ideas):
        idea = come_up_with_idea()
        ideas.append({
            "idea": idea,
            "score": estimate_funniness(idea)
        })
    ideas.sort(key=lambda x: x["score"], reverse=True)
    return ideas[0]["idea"]


def estimate_funniness(idea):
    prompt = [
        {
            "role": "system",
            "content": "You are a humor evaluation expert.\n" +
                       "First, analyze how funny and creative the idea is.\n" +
                       "Then, estimate the quality of an idea with a score from 0 to 100.\n" +
                       "Please be very critical.\n" +
                       "Make sure to include a clear numeric score in your response, formatted as 'Score: X'."
        },
        {
            "role": "user",
            "content": f"Please evaluate how funny this idea is:\n\n{idea}"
        }
    ]

    response = models.call_llm(prompt, estimation_model, 0)

    score_match = re.search(r'Score: (\d+)', response)
    if score_match:
        score = int(score_match.group(1))
        return max(0, min(score, 100))
    else:
        numbers = re.findall(r'\b([0-9]{1,3})\b', response)
        for num in numbers:
            num = int(num)
            if 0 <= num <= 100:
                return num
    return 0


if __name__ == "__main__":
    random.seed(40)
    ideate()
