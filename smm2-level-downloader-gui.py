import os
import json
import requests
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from io import BytesIO

HISTORY_FILE = "history.txt"
SAVE_DIR_FILE = "smm2-save-directory.txt"

# ------------------------------
# Utility Functions
# ------------------------------

def load_history():
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump([], f)
        return []
    with open(HISTORY_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []

def save_history(slot):
    history = load_history()
    if slot not in history:
        history.append(slot)
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f)

def load_save_dir():
    if not os.path.exists(SAVE_DIR_FILE):
        with open(SAVE_DIR_FILE, "w") as f:
            f.write(os.getcwd())
        return os.getcwd()
    with open(SAVE_DIR_FILE, "r") as f:
        return f.read().strip()

def save_save_dir(path):
    with open(SAVE_DIR_FILE, "w") as f:
        f.write(path)

def pad_slot(slot):
    return f"{int(slot):03d}"

# ------------------------------
# API Calls
# ------------------------------

def fetch_level_info(code):
    url = f"https://tgrcode.com/mm2/level_info/{code.lower()}"
    r = requests.get(url)
    if r.status_code != 200:
        raise ValueError("Level info could not be retrieved.")
    return r.json()

def fetch_image_from_api(code, full=False):
    base = "https://tgrcode.com/mm2/level_entire_thumbnail/" if full else "https://tgrcode.com/mm2/level_thumbnail/"
    url = f"{base}{code.lower()}"
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        return Image.open(BytesIO(r.content))
    except:
        return None

def download_level_data(code, save_path):
    url = f"https://tgrcode.com/mm2/level_data/{code.lower()}"
    r = requests.get(url)
    if r.status_code != 200:
        raise ValueError("Level data file could not be downloaded.")
    with open(save_path, "wb") as f:
        f.write(r.content)

# ------------------------------
# GUI Application
# ------------------------------

class LevelDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MM2 Level Downloader")

        self.level_info = None
        self.thumbnail_main = None
        self.thumbnail_full = None

        self.build_gui()

    def build_gui(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(sticky=(N, S, E, W))

        # ------------------------------
        # Level code input
        # ------------------------------
        ttk.Label(frame, text="Enter Level Code (ABCDEFGHI):").grid(row=0, column=0, sticky=W)
        self.code_var = StringVar()
        ttk.Entry(frame, textvariable=self.code_var, width=20).grid(row=0, column=1, sticky=W)
        ttk.Button(frame, text="Fetch Info", command=self.load_level).grid(row=0, column=2, padx=5)

        # ------------------------------
        # Save directory selection
        # ------------------------------
        ttk.Button(frame, text="Select Save Directory", command=self.select_save_dir).grid(row=0, column=3, padx=5)
        self.save_dir_label = Label(frame, text=load_save_dir(), anchor=W)
        self.save_dir_label.grid(row=0, column=4, padx=5, sticky=W)

        # ------------------------------
        # Info panel (scrollable)
        # ------------------------------
        info_frame = Frame(frame)
        info_frame.grid(row=1, column=0, columnspan=5, pady=10, sticky=(N, S, E, W))
        self.info_text = Text(info_frame, width=100, height=15, wrap=WORD)
        self.info_text.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar = Scrollbar(info_frame, command=self.info_text.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.info_text.config(yscrollcommand=scrollbar.set, state=DISABLED)

        # ------------------------------
        # Thumbnail display
        # ------------------------------
        self.image_label = Label(frame)
        self.image_label.grid(row=2, column=0, columnspan=5, pady=10)

        self.btn_show_overview = ttk.Button(frame, text="Show Full Overview", command=self.show_full_overview, state=DISABLED)
        self.btn_show_overview.grid(row=3, column=0)
        self.btn_dl_main = ttk.Button(frame, text="Download Thumbnail", command=self.download_main_thumb, state=DISABLED)
        self.btn_dl_main.grid(row=3, column=1)
        self.btn_dl_full = ttk.Button(frame, text="Download Overview", command=self.download_full_thumb, state=DISABLED)
        self.btn_dl_full.grid(row=3, column=2)

        # ------------------------------
        # Slot selection
        # ------------------------------
        ttk.Label(frame, text="Select Slot (0–179):").grid(row=4, column=0, pady=10, sticky=W)
        self.slot_var = StringVar()
        self.slot_combo = ttk.Combobox(frame, textvariable=self.slot_var, width=10)
        self.slot_combo.grid(row=4, column=1, sticky=W)
        self.slot_combo.config(state="normal")  # allow typing any valid slot

        # Populate dropdown initially
        self.refresh_unused_slots()

        # Download level data button
        ttk.Button(frame, text="Download Level Data", command=self.download_data).grid(row=5, column=0, columnspan=5, pady=10)

    # ------------------------------
    # Refresh unused slots for dropdown
    # ------------------------------
    def refresh_unused_slots(self):
        used = load_history()
        unused_slots = [i for i in range(180) if i not in used]
        self.slot_combo['values'] = unused_slots

    # ------------------------------
    # GUI Logic
    # ------------------------------

    def select_save_dir(self):
        path = filedialog.askdirectory(initialdir=load_save_dir())
        if path:
            save_save_dir(path)
            self.save_dir_label.config(text=path)  # update label
            messagebox.showinfo("Saved", f"Save directory set to:\n{path}")

    def load_level(self):
        code = self.code_var.get().strip()
        if len(code) != 9:
            messagebox.showerror("Error", "Level code must be 9 characters.")
            return

        # Fetch level info
        try:
            self.level_info = fetch_level_info(code)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch level info:\n{e}")
            return

        # Display processed info + raw JSON
        self.info_text.config(state=NORMAL)
        self.info_text.delete(1.0, END)

        processed_info = [
            f"Name: {self.level_info.get('name', 'N/A')}",
            f"Description: {self.level_info.get('description', 'N/A')}",
            f"Game Style: {self.level_info.get('game_style_name', 'N/A')}",
            f"Theme: {self.level_info.get('theme_name', 'N/A')}",
            f"Difficulty: {self.level_info.get('difficulty_name', 'N/A')}",
            f"Uploader: {self.level_info.get('uploader', {}).get('name', 'N/A')} ({self.level_info.get('uploader', {}).get('region_name', 'N/A')})",
            f"Clears / Plays: {self.level_info.get('clears', 0)} / {self.level_info.get('plays', 0)}",
            f"Clear Rate: {self.level_info.get('clear_rate_pretty', 'N/A')}",
            f"Likes / Boos: {self.level_info.get('likes', 0)} / {self.level_info.get('boos', 0)}",
            f"Comments: {self.level_info.get('num_comments', 0)}"
        ]
        self.info_text.insert(END, "\n".join(processed_info))
        self.info_text.insert(END, "\n\nRaw JSON:\n")
        self.info_text.insert(END, json.dumps(self.level_info, indent=2))
        self.info_text.config(state=DISABLED)

        # Load thumbnails
        self.thumbnail_main = fetch_image_from_api(code, full=False)
        self.thumbnail_full = fetch_image_from_api(code, full=True)

        if self.thumbnail_main:
            self.show_image(self.thumbnail_main)
        else:
            self.thumbnail_main = Image.new("RGB", (400, 225), color="gray")
            self.show_image(self.thumbnail_main)

        # Enable buttons appropriately
        self.btn_show_overview.config(state=NORMAL if self.thumbnail_full else DISABLED)
        self.btn_dl_main.config(state=NORMAL if self.thumbnail_main else DISABLED)
        self.btn_dl_full.config(state=NORMAL if self.thumbnail_full else DISABLED)

    def show_image(self, img):
        img_resized = img.resize((400, 225))
        self.tk_img = ImageTk.PhotoImage(img_resized)
        self.image_label.config(image=self.tk_img)

    def show_full_overview(self):
        if not self.thumbnail_full:
            return
        win = Toplevel(self.root)
        win.title("Full Overview")
        img = self.thumbnail_full
        screen_w, screen_h = win.winfo_screenwidth() - 100, win.winfo_screenheight() - 100
        ratio = min(screen_w / img.width, screen_h / img.height, 1)
        img_resized = img.resize((int(img.width * ratio), int(img.height * ratio)))
        tk_img = ImageTk.PhotoImage(img_resized)
        lbl = Label(win, image=tk_img)
        lbl.image = tk_img
        lbl.pack()

    # ------------------------------
    # Download thumbnails
    # ------------------------------
    def download_main_thumb(self):
        code = self.code_var.get().strip().upper()
        if self.thumbnail_main:
            path = os.path.join(load_save_dir(), f"{code}_main_thumb.jpg")
            self.thumbnail_main.save(path)
            messagebox.showinfo("Saved", f"Saved as {path}")

    def download_full_thumb(self):
        code = self.code_var.get().strip().upper()
        if self.thumbnail_full:
            path = os.path.join(load_save_dir(), f"{code}_overview.jpg")
            self.thumbnail_full.save(path)
            messagebox.showinfo("Saved", f"Saved as {path}")

    # ------------------------------
    # Level data download
    # ------------------------------
    def download_data(self):
        code = self.code_var.get().strip().lower()
        slot = self.slot_var.get().strip()
        if not slot.isdigit():
            messagebox.showerror("Error", "Slot must be a number.")
            return

        slot_num = int(slot)
        slot_str = pad_slot(slot)
        save_history(slot_num)
        self.refresh_unused_slots()  # refresh dropdown after marking slot as used

        save_dir = load_save_dir()
        output_path = os.path.join(save_dir, f"course_data_{slot_str}.bcd")

        try:
            download_level_data(code, output_path)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        messagebox.showinfo("Success", f"Downloaded level data to:\n{output_path}")


# ------------------------------
# Run GUI
# ------------------------------
root = Tk()
app = LevelDownloaderGUI(root)
root.mainloop()
