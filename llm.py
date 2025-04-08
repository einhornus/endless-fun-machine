import nlp_library.llm.llm


def call_llm(prompt, model, temp = 0):
    res = nlp_library.llm.llm.call_llm(prompt, model, temp)
    return res