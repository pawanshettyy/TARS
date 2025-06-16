# src/main.py - Main application entry point
import sys
import os
import threading
import time
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from core.tars_brain import TARSBrain
from ui.main_interface import TARSInterface
from utils.logger import setup_logger
from utils.config import Config

class TARSApplication:
    """Main TARS application controller"""
    
    def __init__(self):
        self.config = Config()
        self.logger = setup_logger()
        self.brain = TARSBrain(self.config)
        self.ui = TARSInterface(self.config, self.brain)
        self.running = False
        
    def start(self):
        """Start the TARS system"""
        self.logger.info("Starting TARS Autonomous Robot Platform")
        self.running = True
        
        try:
            # Start brain in separate thread
            brain_thread = threading.Thread(target=self.brain.start, daemon=True)
            brain_thread.start()
            
            # Start UI in main thread
            self.ui.run()
            
        except KeyboardInterrupt:
            self.logger.info("Shutdown requested by user")
        except Exception as e:
            self.logger.error(f"Critical error: {e}")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Graceful shutdown"""
        self.logger.info("Shutting down TARS system")
        self.running = False
        self.brain.stop()
        self.ui.stop()

if __name__ == "__main__":
    app = TARSApplication()
    app.start()