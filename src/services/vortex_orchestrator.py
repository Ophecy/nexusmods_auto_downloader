"""
Vortex mode orchestration service.
"""

import time
import pyautogui
from typing import Optional

from src.domain.downloader_config import DownloaderConfig
from src.infrastructure.input.click_recorder import ClickRecorder
from src.infrastructure.input.keyboard_listener import KeyboardListener
from src.infrastructure.vision.button_detector import ButtonDetector
from src.config.settings import Settings


class VortexOrchestrator:
    """Orchestrates the Vortex two-button monitoring loop."""

    def __init__(self, config: DownloaderConfig):
        self.config = config
        self.keyboard_listener = KeyboardListener()
        self.recorder = ClickRecorder()
        self.nexus_detector = ButtonDetector(config.template_path, config.detection_confidence)
        self.vortex_click_position: Optional[tuple] = None
        self.nexus_click_position: Optional[tuple] = None

    def execute(self) -> None:
        self.keyboard_listener.start()
        print("F4 pour arrêter à tout moment\n")

        if not self._record_positions():
            self.keyboard_listener.stop()
            return

        self._run_monitoring_loop()
        self.keyboard_listener.stop()
        print("\n[DONE] Mode Vortex arrêté.")

    def _record_positions(self) -> bool:
        # Vortex : position fixe uniquement (fenêtre non capturable par screenshot GDI)
        self.vortex_click_position = self.recorder.record_click(
            prompt="Déclenchez un téléchargement dans Vortex.\nCLIQUEZ sur 'DOWNLOAD MANUALLY' dans Vortex."
        )
        if not self.vortex_click_position:
            return False

        # Nexus : position + template (navigateur capturable normalement)
        print("\n" + "="*60)
        print("ÉTAPE 2 — Bouton Nexus 'Slow Download'")
        print("="*60)
        print("Basculez sur l'onglet Nexus Mods ouvert dans le navigateur.")
        input(">>> Appuyez sur ENTRÉE quand le bouton 'SLOW DOWNLOAD' est visible...")
        nexus_screenshot = pyautogui.screenshot()

        self.nexus_click_position = self.recorder.record_click(
            prompt="Cliquez maintenant sur 'SLOW DOWNLOAD' sur Nexus Mods."
        )
        if not self.nexus_click_position:
            return False
        self.nexus_detector.capture_template(self.nexus_click_position, screenshot=nexus_screenshot)

        print("\nPositions enregistrées. Démarrage de la surveillance...\n")
        return True

    def _run_monitoring_loop(self) -> None:
        print(f"Boucle démarrée. Intervalle entre chaque téléchargement : {self.config.delay_for_download}s")
        print("(F4 pour arrêter)\n")

        while not self.keyboard_listener.check_should_stop():
            self._execute_click_sequence()
            if not self.keyboard_listener.check_should_stop():
                time.sleep(self.config.delay_for_download)

    def _execute_click_sequence(self) -> None:
        print(f"  Clic Vortex à {self.vortex_click_position}...")
        pyautogui.click(*self.vortex_click_position)

        time.sleep(Settings.VORTEX_NEXUS_CLICK_DELAY)

        if self.keyboard_listener.check_should_stop():
            return

        nexus_pos = self.nexus_detector.detect_button() or self.nexus_click_position
        if nexus_pos is None:
            print("  AVERTISSEMENT: position Nexus introuvable, clic ignoré.")
            return

        print(f"  Clic Nexus 'Slow Download' à {nexus_pos}...")
        pyautogui.click(*nexus_pos)
        print(f"  Séquence terminée. Prochaine dans {self.config.delay_for_download}s...\n")
