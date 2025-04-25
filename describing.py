import os
import models

model = "anthropic/claude-3.7-sonnet"


def describe_image(image_path):
    prompt = [
        {
            "role": "user",
            "content": f"Here is an image: <image>{image_path}</image>"
        },
        {
            "role": "system",
            "content": "You are an image explainer.\n" +
                       f"Please describe the image provided in full details focusing on what makes the image funny, and then summarize the idea of the image.\n" +
                       "Response format:\n" +
                       "<Detailed image description>\n" +
                       "Summary: "
                       "```\n" +
                       "<Summary of the image idea>\n" +
                       "```\n"
        }
    ]

    res = models.call_llm(prompt, model)
    if res.count("```") >= 2:
        last_idx = res.rfind("```")
        penultimate_idx = res.rfind("```", 0, last_idx)
        summary = res[penultimate_idx + 3:last_idx]
    else:
        summary = res
    summary = summary.strip()
    return summary


def remove_txt_files(directory):
    count = 0
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) and filename.endswith('.txt'):
                os.remove(file_path)
                print(f"Removed: {file_path}")
                count += 1
        print(f"Total: {count} .txt files removed from {directory}")
        return count
    except Exception as e:
        print(f"Error: {e}")
        return 0


def describe_all_images(directory):
    count = 0
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) and filename.lower().endswith('.png'):
                description = describe_image(file_path)

                base_name = os.path.splitext(filename)[0]
                txt_file_path = os.path.join(directory, f"{base_name}.txt")
                with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(description)

                print(f"Processed: {file_path} -> {txt_file_path}")
                count += 1

        print(f"Total: {count} images processed in {directory}")
        return count
    except Exception as e:
        print(f"Error processing images: {e}")
        return 0


if __name__ == "__main__":
    remove_txt_files("data")
    describe_all_images("data")
