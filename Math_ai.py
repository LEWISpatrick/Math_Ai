import tkinter as tk
from PIL import ImageGrab, ImageTk
import pytesseract


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

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def capture_screen(self):
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

    def start_selection(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def update_selection(self, event):
        if self.selection_rect:
            self.screenshot_canvas.delete(self.selection_rect)
        self.end_x = event.x
        self.end_y = event.y
        self.selection_rect = self.screenshot_canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline="red")

    def end_selection(self, event):
        if self.selection_rect:
            self.screenshot_canvas.delete(self.selection_rect)
        self.end_x = event.x
        self.end_y = event.y
        self.process_selection()

    def process_selection(self):
        if self.start_x is not None and self.start_y is not None and self.end_x is not None and self.end_y is not None:
            screenshot = ImageGrab.grab()
            selected_region = screenshot.crop((self.start_x, self.start_y, self.end_x, self.end_y))
            extracted_text = pytesseract.image_to_string(selected_region)
            print(extracted_text)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ScreenCaptureApp()
    app.run()
