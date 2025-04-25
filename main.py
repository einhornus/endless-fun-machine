import ideation
import implementation
import models
import os

if __name__ == "__main__":
    pic_count = 5
    os.makedirs("all_results/results", exist_ok=True)
    for i in range(pic_count):
        idea = ideation.ideate()
        print("Idea")
        print(idea)
        print("\n-----------------\n")
        image_prompt = implementation.implement_idea(idea)
        print("Image prompt")
        print(image_prompt)

        with open(f"all_results/results//{i}_idea.txt", "w", encoding="utf-8") as idea_file:
            idea_file.write(idea)
        with open(f"all_results/results//{i}_prompt.txt", "w", encoding="utf-8") as prompt_file:
            prompt_file.write(image_prompt)

        try:
            models.gen_image(image_prompt, f"all_results/results//{i}.png")
        except Exception as e:
            print(e)
            print("Can't generate image")
        print("\n\n\n\n")
