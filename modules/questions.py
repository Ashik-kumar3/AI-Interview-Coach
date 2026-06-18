def load_questions(filepath):

    print("Loading:", filepath)

    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    print("FILE CONTENTS:")
    print(repr(content))

    questions = [
        line.strip()
        for line in content.splitlines()
        if line.strip()
    ]

    return questions