import tkinter as tk
from PIL import ImageGrab, ImageTk
import pytesseract


class SelectedTextApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Selected Text")
        self.root.geometry("400x300")

        self.text_widget = tk.Text(self.root, wrap=tk.WORD)
        self.text_widget.pack(fill=tk.BOTH, expand=True)

    def set_text(self, text):
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, text)


class ScreenCaptureApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Screen Capture App")
        self.root.geometry("600x400")

        self.screenshot_canvas = tk.Canvas(self.root)
        self.screenshot_canvas.pack()

        capture_button = tk.Button(self.root, text="Capture", command=self.capture_screen)
        capture_button.pack(pady=10)

        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.selection_rect = None

        self.selected_text_app = SelectedTextApp()

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def capture_screen(self):
        try:
            self.root.withdraw()
            self.root.update()

            screen = ImageGrab.grab()
            self.screenshot_image = ImageTk.PhotoImage(screen)

            self.screenshot_canvas.config(width=self.screenshot_image.width(), height=self.screenshot_image.height())
            self.screenshot_canvas.create_image(0, 0, image=self.screenshot_image, anchor=tk.NW)

            self.root.deiconify()

            self.screenshot_canvas.bind("<Button-1>", self.start_selection)
            self.screenshot_canvas.bind("<B1-Motion>", self.update_selection)
            self.screenshot_canvas.bind("<ButtonRelease-1>", self.end_selection)
        except Exception as e:
            print("Error capturing the screen:", str(e))

    def start_selection(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def update_selection(self, event):
        if self.selection_rect:
            self.screenshot_canvas.delete(self.selection_rect)
        self.end_x = event.x
        self.end_y = event.y
        self.selection_rect = self.screenshot_canvas.create_rectangle(
            self.start_x, self.start_y, self.end_x, self.end_y, outline="red"
        )

    def end_selection(self, event):
        if self.selection_rect:
            self.screenshot_canvas.delete(self.selection_rect)
        self.end_x = event.x
        self.end_y = event.y
        self.process_selection()

        if self.selected_text_app.root.winfo_exists():
            self.capture_screen()

    def process_selection(self):
        if self.start_x is not None and self.start_y is not None and self.end_x is not None and self.end_y is not None:
            try:
                screenshot = ImageGrab.grab()
                selected_region = screenshot.crop((self.start_x, self.start_y, self.end_x, self.end_y))
                extracted_text = pytesseract.image_to_string(selected_region)
                self.selected_text_app.set_text(extracted_text)  # Set the text in SelectedTextApp
            except Exception as e:
                print("Error processing the selection:", str(e))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ScreenCaptureApp()
    app.run()

