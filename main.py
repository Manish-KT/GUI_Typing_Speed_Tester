import tkinter as tk
import requests
import time


class TypingSpeedTestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.number_of_paragraphs_entry = 1
        self.number_of_paragraphs_label = None
        self.fetch_paragraph_button = None
        self.title("Typing Speed Test")
        self.geometry("800x800")
        self.api_url = f"https://baconipsum.com/api/?type=meat-and-filler&paras={self.number_of_paragraphs_entry}"
        self.current_paragraph = ""
        self.start_time = 0
        self.typing_entry = None
        self.paragraph_label = None
        self.result_label = None

        self.create_widgets()
        self.new_paragraph()

    def create_widgets(self):
        # create a widget for getting number of paragraphs from user and default value is 1
        self.number_of_paragraphs_label = tk.Label(self, text="Number of paragraphs", font=("Helvetica", 14))
        self.number_of_paragraphs_label.pack(pady=10)

        self.number_of_paragraphs_entry = tk.Entry(self, font=("Helvetica", 14))
        self.number_of_paragraphs_entry.pack(pady=10)
        self.number_of_paragraphs_entry.insert(0, "1")
        self.number_of_paragraphs_entry.bind("<Return>", self.update_number_of_paragraphs)

        self.paragraph_label = tk.Label(self, text="", font=("Helvetica", 14), wraplength=700, justify=tk.LEFT)
        self.paragraph_label.pack(pady=20)

        self.typing_entry = tk.Text(self, font=("Helvetica", 14), height=2 * self.number_of_paragraphs_entry.get(),
                                    width=50)
        self.typing_entry.pack(pady=10)
        self.typing_entry.bind("<Return>", self.check_typing)

        self.result_label = tk.Label(self, text="", font=("Helvetica", 18))
        self.result_label.pack(pady=20)

        self.fetch_paragraph_button = tk.Button(self, text="Fetch new paragraph", command=self.new_paragraph)
        self.fetch_paragraph_button.pack(pady=10)

    def update_number_of_paragraphs(self, event):
        self.api_url = f"https://baconipsum.com/api/?type=meat-and-filler&paras={self.number_of_paragraphs_entry.get()}"
        print(self.api_url)

    def fetch_paragraph(self):
        self.update_number_of_paragraphs(self)
        response = requests.get(self.api_url)
        if response.status_code == 200:
            data = response.json()
            self.current_paragraph = data[0]
            self.paragraph_label.config(text=self.current_paragraph)

    def new_paragraph(self):
        self.fetch_paragraph()
        self.typing_entry.delete(1.0, tk.END)
        self.start_time = time.time()

    def check_typing(self, event):
        typed_paragraph = self.typing_entry.get().strip()

        if typed_paragraph == self.current_paragraph:
            elapsed_time = time.time() - self.start_time
            speed = len(typed_paragraph.split()) / (elapsed_time / 60)  # Speed in words per minute
            self.result_label.config(text=f"Your typing speed: {speed:.2f} WPM")
        else:
            self.result_label.config(text="Incorrect. Try again.")

        self.after(1500, self.new_paragraph)  # Wait for 1.5 seconds and then fetch a new paragraph


if __name__ == "__main__":
    app = TypingSpeedTestApp()
    app.mainloop()
