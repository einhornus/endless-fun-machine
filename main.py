import ideation
import implementation

if __name__ == "__main__":
    idea = ideation.ideate(10)
    print(idea)
    print("----")
    image_prompt = implementation.implement_idea(idea)
    print(image_prompt)