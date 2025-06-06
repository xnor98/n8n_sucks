from openai import OpenAI

XAI_API_KEY = "xai-1OXq3qIg8ecSumNwqawHwAJg25Rs3YugtRGzBvqZPKzRc13QPucfQxI99SU4VHE7XP2LnxPVWWyI1pPe"

SUBJECT = input("sujet> ")

client = OpenAI(
  api_key=XAI_API_KEY,
  base_url="https://api.x.ai/v1",
)


def create_books_collection(subject):
    print("Génération des titres des différents livres...")

    books = {}

    prompt="""
    ### Find 10 chapters to explain the given topic logically, you will only return the chapter titles without numbering them and without saying anything else.

    subject : """+subject

    completion = client.chat.completions.create(
        model="grok-3-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    generated_books_titles = completion.choices[0].message.content

    with open("books_titles.txt", "w") as file:
        file.write(completion.choices[0].message.content)

    temp_title = ""
    for char in generated_books_titles:
        if char == "\n":
            books[temp_title] = []
            temp_title = ""
        else:
            temp_title += char

    return books 

def create_chapters_for_books(subject, books):
    books_with_subjects = books

    for book in books_with_subjects:
        prompt="""
        ### Find 10 chapters to explain the given topic logically, you will only return the chapter titles without numbering them and without saying anything else.

        subject : """+subject

    return books_with_subjects

books = create_books_collection(SUBJECT)
books_with_subjects = create_chapters_for_books(SUBJECT, books)
