import tkinter as tk
from tkinter import Label, PhotoImage
import pandas as pd
from PIL import Image, ImageTk, ImageDraw, ImageFont

class App:
    def handle_keypress(self, event):
        if event.keysym == 'f':
            self.skip_gender()
        elif event.keysym == 'Right':
            self.next_image_same_id()
        elif event.keysym == 'Left':
            self.prev_image_same_id()

    def __init__(self, root, labels_file, image_dir):
        
        # Read labels from CSV
        self.df = pd.read_csv(labels_file)
        self.df.sort_values(by=['frame_num', 'id'], inplace=True)
        self.image_dir = image_dir
        
        self.current_index = 550
        self.processed_ids = (set(range(1,self.current_index)))
        # Load the first image
        self.load_image()

        # Create UI
        self.label_id = Label(root, text=f"ID: {int(self.current_id())}", font=("Arial", 16, "bold"))
        self.label_id.pack()

        self.canvas = tk.Canvas(root, width=self.image_obj.width(), height=self.image_obj.height())
        self.canvas.pack()
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind_all("<Key>", self.handle_keypress)
        self.update_image()

    def load_image(self):
        frame_num = self.df.iloc[self.current_index]['frame_num']
        image_file = f"{int(frame_num)}_with_boxes.jpeg"
        self.image_path = f"{self.image_dir}/{image_file}"
        image = Image.open(self.image_path)
        self.image_obj = ImageTk.PhotoImage(image)
        self.img_width, self.img_height = image.size

    def on_click(self, event):
        if event.x > self.img_width // 2:
            self.fill_gender(self.current_id(), 0)
        else:
            self.fill_gender(self.current_id(), 1)
        
        self.next_image()

    def skip_gender(self):
        self.fill_gender(self.current_id(), 2)
        self.next_image()

    def fill_gender(self, id_value, side):
        self.last_side = side
        print(id_value)
        print(side)
        self.processed_ids.add(id_value)  # Add ID to processed set
        if side==2: return
        self.df.loc[self.df['id'] == id_value, 'gender'] = int(side)
        self.df.to_csv(f'./labels.csv',index=False)

    def current_id(self):
        return self.df.iloc[self.current_index]['id']

    def next_image(self):
        self.current_index += 1
        while self.current_index < len(self.df) and self.current_id() in self.processed_ids:
            self.current_index += 1  # Increment the index if ID already processed

        if self.current_index >= len(self.df):
            print("All images processed")
            return

        self.load_image()
        self.update_image()

    def next_image_same_id(self):
        current_id_val = self.current_id()
        
        # Store the starting index as a safeguard
        starting_index = self.current_index

        while self.current_index < len(self.df) - 1:
            self.current_index += 1
            if self.df.iloc[self.current_index]['id'] == current_id_val:
                break

        # If the next image's id doesn't match the current id, revert back to the starting index
        if self.df.iloc[self.current_index]['id'] != current_id_val:
            self.current_index = starting_index

        self.load_image()
        self.update_image()

    def prev_image_same_id(self):
        current_id_val = self.current_id()
        
        # Store the starting index as a safeguard
        starting_index = self.current_index

        while self.current_index > 0:
            self.current_index -= 1
            if self.df.iloc[self.current_index]['id'] == current_id_val:
                break

        # If the previous image's id doesn't match the current id, revert back to the starting index
        if self.df.iloc[self.current_index]['id'] != current_id_val:
            self.current_index = starting_index

        self.load_image()
        self.update_image()


    def update_image(self):
        self.canvas.create_image(0, 0, anchor="nw", image=self.image_obj)
        self.label_id.config(text=f"ID: {int(self.current_id())}/5965")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root, './labels.csv', './detected_obj_frames/spbpu1/SPBPU1_24_03_2023__08_37_44_1080_people')
    root.mainloop()
