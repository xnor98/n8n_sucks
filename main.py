from openai import OpenAI

XAI_API_KEY = "xai-RpmzdIYF09uIErZ2btAWQrCiv2MdA11WKiS5b6tkNMJd0YsW4MKX5UUyEuJSTd9ra4fykDWqCpVpDKDj"

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

    return books, generated_books_titles

def create_chapters_for_books(subject, books, strbooks):
    print("Génération des chapitres pour chaque livres...")
    books_with_subjects = books

    for book in books_with_subjects:
        print(f"Génération des chapitres pour le livre -> {book}")

        prompt=f"""
        You must write between 5 and 10 chapter titles that could fit into the book " {book} " that belongs to the following book collection:
        {strbooks}
        The main subject of this book collection is {subject}.
        The chapter titles must be coherent, you will write only the chapter titles and nothing else. 
        You will write the number of the chapter like this:
        1 - replace with chapter name
        2 - replace with chapter name
        3 - replace with chapter name
        etc
        """
        completion = client.chat.completions.create(
            model="grok-3-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        generated_chapters_titles = completion.choices[0].message.content

        temp_title = ""
        for char in generated_chapters_titles:
            if char == "\n":
                books_with_subjects[book].append(temp_title)
                temp_title = ""
            else:
                temp_title += char


    return books_with_subjects

def summary_print(bws):
    summary = ""
    for book in bws:
        summary += "Book: "+ book + "\n"
        for chap in bws[book]:
            summary += "     Chapter: "+chap+"\n"

def chapter_content_generator(bws, subject, summary):
    
    for book in bws:
        for chapter in bws[book]:

            prompt = f"""
            You have to write the contents of the chapter "{chapter}" in the book "{book}".
            Here is the table of contents of the book collection, I give it to you as a context:

            {summary}

            ### WARNING
            You must write only the contents of chapter "{chapter}" and not the contents of the other chapters.
            You must be as detailed as possible in your explanations.
            You must use markdown format when writing.
            You'll return the chapter content directly and nothing else.
            You can use emoji to enhance your content.
            When writing don't forget the main subject “{subject}”.
            """

            completion = client.chat.completions.create(
                model="grok-3-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            chapter_content = completion.choices[0].message.content

            print("Livre | {book} | Chapitre | {chapter} | Génération terminée !")
            fn = book+".md"
            with open(fn, "a") as file:
                file.write(f"""
                # {book}
                ## {chapter}



                {chapter_content}
                """)
            


books, strbooks = create_books_collection(SUBJECT)
books_with_subjects = create_chapters_for_books(SUBJECT, books, strbooks)

print("Tout les titres des livres et des chapitres ont été générés.")
print("Voulez vous voir le sommaire de votre collection de livres ?")
rep1 = input("voir le sommaire ? (y/n) > ")

summary = summary_print(books_with_subjects)


rep1 = input("voir le sommaire ? (y/n) > ")
if rep1 == "y":
    print(summary)

input("(entre pour continuer)")

print("La génération du contenu de chaque chapitre va commencer...")

chapter_content_generator(books_with_subjects, SUBJECT, summary)
