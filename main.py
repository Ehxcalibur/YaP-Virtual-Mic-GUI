import logging
from src.gui import App

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Starting YaP Audio - Void Mic")
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
