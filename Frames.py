from tkinter import *
from tkinter import filedialog, messagebox, ttk
import random
import imageio
import os

class VideoFrameExtractor:
    def __init__(self):
        self.window = Tk() 
        self.window.title("Video Frame Extractor")
        self.video_file_path = StringVar()
        self.frames_to_save = StringVar()
        self.random_seed = StringVar(value="123")    # default seed
        self.destination_folder_path = StringVar()

        Label(self.window, text="Video File Path:").grid(row=0)
        Entry(self.window, textvariable=self.video_file_path).grid(row=0, column=1)
        Button(self.window, text="Browse", command=self.browse_video_file).grid(row=0, column=2)

        Label(self.window, text="No. of Frames to save:").grid(row=1)
        Entry(self.window, textvariable=self.frames_to_save).grid(row=1, column=1)

        Label(self.window, text="Seed for randomizer:").grid(row=2)    # Seed input
        Entry(self.window, textvariable=self.random_seed).grid(row=2, column=1)

        Label(self.window, text="Destination Folder Path:").grid(row=3)
        Entry(self.window, textvariable=self.destination_folder_path).grid(row=3, column=1)
        Button(self.window, text="Browse", command=self.browse_destination_folder).grid(row=3, column=2)

        Button(self.window, text="Extract", command=self.extract_frames).grid(row=4, column=1)

        # Progress bar
        self.progress = ttk.Progressbar(self.window, orient="horizontal", length=200, mode='determinate')
        self.progress.grid(row=5, columnspan=3, padx=10, pady=10)

    def browse_video_file(self):
        self.video_file_path.set(filedialog.askopenfilename())
        
    def browse_destination_folder(self):
        self.destination_folder_path.set(filedialog.askdirectory())

    def extract_frames(self):
        seed = self.random_seed.get().strip()
        if not seed.isdigit():
            messagebox.showerror("Error", "Seed must be an integer.")
            return
        random.seed(int(seed))    # Set the seed

        vid_reader = imageio.get_reader(self.video_file_path.get())
        total_frames = vid_reader.count_frames()

        if total_frames < int(self.frames_to_save.get()):
            vid_reader.close()
            messagebox.showerror("Error", "Number of frames to extract is greater than total frames in the video.")
            return

        frames_list = sorted(random.sample(range(total_frames), k=int(self.frames_to_save.get())))
        self.progress["maximum"] = len(frames_list)

        for i, frame_no in enumerate(frames_list):
            img = vid_reader.get_data(frame_no)
            imageio.imwrite(os.path.join(self.destination_folder_path.get(), f'frame_{frame_no}.jpg'), img)

            # Update the progress bar
            self.progress["value"] = i+1
            self.progress.update()

        vid_reader.close()
        self.progress["value"] = 0    # Reset the progressbar
        messagebox.showinfo('Done', 'Frame Extraction Completed Successfully.')
        
if __name__ == "__main__":
    VideoFrameExtractor().window.mainloop()