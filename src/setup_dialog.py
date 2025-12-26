import customtkinter as ctk
import os
import sys

# Theme Colors
VOID_BLACK = "#000000"
DEEP_EERIE_BLACK = "#1C1C1C"
ELECTRIC_VIOLET = "#8F00FF"
PHLOX_PURPLE = "#DF00FF"
PALE_VIOLET = "#E0B3F7"

class SetupDialog(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Setup - Void Mic")
        self.geometry("400x200")
        self.resizable(False, False)
        
        # Theme
        ctk.set_appearance_mode("Dark")
        self.configure(fg_color=VOID_BLACK)

        self._create_widgets()
        
        # Center on screen
        self.eval('tk::PlaceWindow . center')

    def _create_widgets(self):
        self.main_frame = ctk.CTkFrame(self, fg_color=DEEP_EERIE_BLACK, corner_radius=15)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label = ctk.CTkLabel(
            self.main_frame,
            text="Create Desktop Shortcut?",
            font=("Roboto Medium", 18),
            text_color=PALE_VIOLET
        )
        self.label.pack(pady=(30, 20))

        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_frame.pack(pady=10)

        self.btn_yes = ctk.CTkButton(
            self.btn_frame,
            text="YES",
            command=self.create_shortcut,
            fg_color=ELECTRIC_VIOLET,
            hover_color=PHLOX_PURPLE,
            text_color="white",
            width=100
        )
        self.btn_yes.grid(row=0, column=0, padx=10)

        self.btn_no = ctk.CTkButton(
            self.btn_frame,
            text="NO",
            command=self.close_app,
            fg_color="transparent",
            border_width=1,
            border_color=ELECTRIC_VIOLET,
            text_color=PALE_VIOLET,
            hover_color=DEEP_EERIE_BLACK,
            width=100
        )
        self.btn_no.grid(row=0, column=1, padx=10)

    def create_shortcut(self):
        try:
            home_dir = os.path.expanduser("~")
            desktop_dir = os.path.join(home_dir, "Desktop")
            app_dir = os.getcwd()
            launch_script = os.path.join(app_dir, "launch.sh")
            
            shortcut_content = f"""[Desktop Entry]
Name=Void Mic
Comment=Virtual Audio Routing Application
Exec={launch_script}
Icon=audio-input-microphone
Terminal=false
Type=Application
Categories=Audio;AudioVideo;
Keywords=mic;virtual;audio;pipewire;
"""
            shortcut_path = os.path.join(desktop_dir, "YaP_Audio.desktop")
            
            with open(shortcut_path, "w") as f:
                f.write(shortcut_content)
            
            # Make executable
            os.chmod(shortcut_path, 0o755)
            
            print(f"Shortcut created at {shortcut_path}")
            self.destroy()
            
        except Exception as e:
            print(f"Failed to create shortcut: {e}")
            self.destroy()

    def close_app(self):
        self.destroy()

if __name__ == "__main__":
    app = SetupDialog()
    app.mainloop()
