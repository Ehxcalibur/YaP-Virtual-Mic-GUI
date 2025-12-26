import customtkinter as ctk
from tkinter import filedialog
import threading
import logging
import time

from .audio import AudioController
from .player import MediaPlayer

# Theme Colors
VOID_BLACK = "#000000"
DEEP_EERIE_BLACK = "#1C1C1C"
ELECTRIC_VIOLET = "#8F00FF"
PHLOX_PURPLE = "#DF00FF"
PALE_VIOLET = "#E0B3F7"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Void Mic - Virtual Audio Injector")
        self.geometry("600x450")
        self.resizable(False, False)
        
        # Audio Backend
        self.audio_controller = AudioController()
        self.media_player = MediaPlayer(sink_name=self.audio_controller.sink_name)

        # Initialize Virtual Devices
        self.audio_controller.setup_virtual_devices()

        # Theme Configuration
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue") # We will override execution manually

        self.configure(fg_color=VOID_BLACK)

        self._create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _create_widgets(self):
        # Main Container
        self.main_frame = ctk.CTkFrame(self, fg_color=DEEP_EERIE_BLACK, corner_radius=15)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Header
        self.label_title = ctk.CTkLabel(
            self.main_frame, 
            text="VOID MIC", 
            font=("Roboto Medium", 24),
            text_color=PHLOX_PURPLE
        )
        self.label_title.pack(pady=(20, 10))

        # Status Label
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Ready to inject audio...",
            text_color=PALE_VIOLET
        )
        self.status_label.pack(pady=(0, 20))

        # URL Input
        self.url_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Paste YouTube URL or select file...",
            width=400,
            fg_color="black",
            border_color=ELECTRIC_VIOLET,
            text_color="white"
        )
        self.url_entry.pack(pady=10)

        # Controls Row
        self.controls_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.controls_frame.pack(pady=10)

        self.btn_file = ctk.CTkButton(
            self.controls_frame,
            text="Browse File",
            command=self.browse_file,
            fg_color=ELECTRIC_VIOLET,
            hover_color=PHLOX_PURPLE,
            text_color="white"
        )
        self.btn_file.grid(row=0, column=0, padx=10)

        self.btn_play = ctk.CTkButton(
            self.controls_frame,
            text="PLAY",
            command=self.play_audio,
            fg_color=ELECTRIC_VIOLET,
            hover_color=PHLOX_PURPLE,
            text_color="white",
            width=80
        )
        self.btn_play.grid(row=0, column=1, padx=10)

        self.btn_stop = ctk.CTkButton(
            self.controls_frame,
            text="STOP",
            command=self.stop_audio,
            fg_color="red",
            hover_color="#8B0000",
            text_color="white",
            width=80
        )
        self.btn_stop.grid(row=0, column=2, padx=10)

        # Volume Slider
        self.volume_label = ctk.CTkLabel(self.main_frame, text="Volume", text_color=PALE_VIOLET)
        self.volume_label.pack(pady=(20, 0))
        
        self.slider_volume = ctk.CTkSlider(
            self.main_frame,
            from_=0,
            to=100,
            command=self.change_volume,
            progress_color=PHLOX_PURPLE,
            button_color=ELECTRIC_VIOLET,
            button_hover_color=PHLOX_PURPLE
        )
        self.slider_volume.set(80) 
        self.slider_volume.pack(pady=5)

        # Monitoring Switch
        self.switch_monitor = ctk.CTkSwitch(
            self.main_frame,
            text="Monitor Audio (Hear it locally)",
            command=self.toggle_monitoring,
            progress_color=ELECTRIC_VIOLET,
            button_color=PHLOX_PURPLE,
            button_hover_color="white",
            text_color=PALE_VIOLET
        )
        self.switch_monitor.pack(pady=20)

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=(("Audio Files", "*.mp3 *.wav *.flac *.m4a *.ogg"), ("All Files", "*.*"))
        )
        if filename:
            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, filename)

    def play_audio(self):
        resource = self.url_entry.get()
        if not resource:
            self.status_label.configure(text="Please enter a URL or select a file!")
            return

        self.status_label.configure(text="Loading stream...")
        
        # Run play in thread to avoid freezing UI
        threading.Thread(target=self._play_thread, args=(resource,), daemon=True).start()

    def _play_thread(self, resource):
        try:
            self.media_player.stop() # Stop any current
            self.media_player.set_volume(self.slider_volume.get())
            self.media_player.play(resource)
            
            # Simple metadata update loop (could be better with observers but this is safe)
            time.sleep(1)
            meta = self.media_player.get_metadata()
            if meta and 'title' in meta:
               self.status_label.configure(text=f"Playing: {meta['title']}")
            else:
               self.status_label.configure(text="Playing...")

        except Exception as e:
            self.status_label.configure(text=f"Error: {e}")

    def stop_audio(self):
        self.media_player.stop()
        self.status_label.configure(text="Stopped.")

    def change_volume(self, value):
        self.media_player.set_volume(value)

    def toggle_monitoring(self):
        enabled = self.switch_monitor.get() == 1
        self.audio_controller.toggle_monitoring(enabled)

    def on_closing(self):
        self.status_label.configure(text="Cleaning up...")
        self.media_player.terminate()
        self.audio_controller.cleanup()
        self.destroy()
