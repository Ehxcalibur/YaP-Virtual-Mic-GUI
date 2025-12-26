import subprocess
import logging

class AudioController:
    def __init__(self):
        self.sink_name = "VoidMic"
        self.source_name = "VoidMicInput"
        self.sink_module_id = None
        self.source_module_id = None
        self.loopback_module_id = None

    def _run_pactl(self, args):
        try:
            result = subprocess.run(
                ["pactl"] + args,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logging.error(f"pactl command failed: {e.cmd} -> {e.stderr}")
            return None

    def setup_virtual_devices(self):
        """Creates the null sink and the remapped source."""
        # 1. Create Null Sink
        # Check if already exists?
        
        logging.info("Creating Null Sink...")
        out_sink = self._run_pactl([
            "load-module", "module-null-sink",
            f"sink_name={self.sink_name}",
            "sink_properties=device.description=Void-Virtual-Mic"
        ])
        if out_sink:
            self.sink_module_id = out_sink
            logging.info(f"Null Sink created with ID: {self.sink_module_id}")

        # 2. Create Remap Source
        logging.info("Creating Remap Source...")
        out_source = self._run_pactl([
            "load-module", "module-remap-source",
            f"master={self.sink_name}.monitor",
            f"source_name={self.source_name}",
            "source_properties=device.description=Void-Virtual-Input"
        ])
        if out_source:
            self.source_module_id = out_source
            logging.info(f"Remap Source created with ID: {self.source_module_id}")

    def toggle_monitoring(self, enabled: bool):
        """Toggles the loopback module for monitoring."""
        if enabled:
            if self.loopback_module_id:
                return # Already enabled
            
            logging.info("Enabling Monitoring...")
            # Route from monitor of null sink to default sink
            out_loop = self._run_pactl([
                "load-module", "module-loopback",
                f"source={self.sink_name}.monitor",
                "sink=@DEFAULT_SINK@",
                "latency_msec=10"
            ])
            if out_loop:
                self.loopback_module_id = out_loop
                logging.info(f"Loopback module created with ID: {self.loopback_module_id}")
        else:
            if self.loopback_module_id:
                logging.info("Disabling Monitoring...")
                self._run_pactl(["unload-module", self.loopback_module_id])
                self.loopback_module_id = None

    def cleanup(self):
        """Unloads all modules created by this session."""
        logging.info("Cleaning up audio modules...")
        if self.loopback_module_id:
            self._run_pactl(["unload-module", self.loopback_module_id])
        if self.source_module_id:
            self._run_pactl(["unload-module", self.source_module_id])
        if self.sink_module_id:
            self._run_pactl(["unload-module", self.sink_module_id])
