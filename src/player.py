import mpv
import logging
import os

class MediaPlayer:
    def __init__(self, sink_name="VoidMic"):
        self.sink_name = sink_name
        self.mpv_instance = None
        self._init_mpv()

    def _init_mpv(self):
        try:
            # Initialize MPV with specific PulseAudio output to our sink
            self.mpv_instance = mpv.MPV(
                ytdl=True,
                input_default_bindings=True,
                input_vo_keyboard=True,
                osc=True,
                vo='null', # Disable video output window
                video=False
            )
            # Route audio to the virtual sink
            # pulse::VoidMic
            self.mpv_instance.audio_device = f"pulse/{self.sink_name}"
            
            @self.mpv_instance.property_observer('percent-pos')
            def time_observer(_name, value):
                pass # Can be used to update GUI progress bar

            @self.mpv_instance.property_observer('core-idle')
            def idle_observer(_name, value):
                if value:
                    logging.info("MPV is idle.")

        except Exception as e:
            logging.error(f"Failed to initialize MPV: {e}")

    def play(self, resource):
        """Plays a local file or URL."""
        if not self.mpv_instance:
            return

        logging.info(f"Playing resource: {resource}")
        self.mpv_instance.play(resource)

    def stop(self):
        if self.mpv_instance:
            self.mpv_instance.stop()

    def set_volume(self, volume):
        """Sets volume (0-100)."""
        if self.mpv_instance:
            self.mpv_instance.volume = volume

    def get_metadata(self):
        if self.mpv_instance:
            return self.mpv_instance.metadata
        return None

    def terminate(self):
        if self.mpv_instance:
            self.mpv_instance.terminate()
