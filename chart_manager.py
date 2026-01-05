import matplotlib.pyplot as plt

def show_books_pie_chart(books, borrowed_books):
    labels = ["Available", "Borrowed"]
    available = len(books) - len(borrowed_books)
    sizes = [available, len(borrowed_books)]
    colors = ["#66b3ff", "#ff9999"]

    plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    plt.title("نسبة الكتب المستعارة مقابل المتاحة")
    plt.axis("equal")  # يجعل الدائرة متوازنة
    plt.show()
