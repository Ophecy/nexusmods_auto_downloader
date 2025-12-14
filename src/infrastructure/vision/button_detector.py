"""
Button detection using OpenCV template matching.
"""

import cv2
import numpy as np
import pyautogui
from pathlib import Path
from typing import Optional


class ButtonDetector:
    """Detects button on screen using template matching."""

    def __init__(self, template_path: str, confidence_threshold: float = 0.8):
        """
        Initialize button detector.

        Args:
            template_path: Path to template image file (normal version)
            confidence_threshold: Minimum confidence for detection (0-1)
        """
        self.template_path = template_path
        self.confidence_threshold = confidence_threshold
        self.normal_template = None
        self.hover_template = None
        self._load_templates()

    def _get_hover_template_path(self) -> str:
        """Get path for hover version of template."""
        path = Path(self.template_path)
        return str(path.parent / f"{path.stem}_hover{path.suffix}")

    def _load_templates(self):
        """Load both normal and hover template images if they exist."""
        if Path(self.template_path).exists():
            try:
                self.normal_template = cv2.imread(self.template_path, cv2.IMREAD_GRAYSCALE)
                if self.normal_template is None:
                    print(f"Warning: Could not load normal template from {self.template_path}")
            except Exception as e:
                print(f"Warning: Normal template loading failed: {e}")
                self.normal_template = None

        hover_path = self._get_hover_template_path()
        if Path(hover_path).exists():
            try:
                self.hover_template = cv2.imread(hover_path, cv2.IMREAD_GRAYSCALE)
                if self.hover_template is None:
                    print(f"Warning: Could not load hover template from {hover_path}")
            except Exception as e:
                print(f"Warning: Hover template loading failed: {e}")
                self.hover_template = None

    def _match_template(self, template, screen_gray) -> tuple:
        """
        Match a single template against screen.

        Args:
            template: Template image in grayscale
            screen_gray: Screen image in grayscale

        Returns:
            Tuple of (confidence_score, (x, y)) or (0.0, None)
        """
        if template is None:
            return (0.0, None)

        try:
            result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val >= self.confidence_threshold:
                template_h, template_w = template.shape
                center_x = max_loc[0] + template_w // 2
                center_y = max_loc[1] + template_h // 2
                return (max_val, (center_x, center_y))

            return (max_val, None)

        except Exception as e:
            print(f"Warning: Template matching failed: {e}")
            return (0.0, None)

    def detect_button(self) -> Optional[tuple]:
        """
        Detect button on screen using template matching.
        Tries both normal and hover templates, returns best match.

        Returns:
            Tuple of (x, y) coordinates at button center, or None if not found
        """
        if self.normal_template is None and self.hover_template is None:
            return None

        try:
            screenshot = pyautogui.screenshot()
            screen_np = np.array(screenshot)
            screen_bgr = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
            screen_gray = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2GRAY)

            normal_conf, normal_pos = self._match_template(self.normal_template, screen_gray)
            hover_conf, hover_pos = self._match_template(self.hover_template, screen_gray)

            if normal_pos is not None and hover_pos is not None:
                return normal_pos if normal_conf >= hover_conf else hover_pos
            elif normal_pos is not None:
                return normal_pos
            elif hover_pos is not None:
                return hover_pos
            else:
                return None

        except Exception as e:
            print(f"Warning: Button detection failed: {e}")
            return None

    def capture_template(self, click_position: tuple, region_size: tuple = (200, 100)) -> bool:
        """
        Capture button template from screen at click position.

        Args:
            click_position: (x, y) where user clicked
            region_size: (width, height) of region to capture around click

        Returns:
            True if template saved successfully, False otherwise
        """
        try:
            template_file = Path(self.template_path)

            if template_file.exists():
                print(f"Template already exists at {self.template_path}, skipping capture to preserve original.")
                return True

            template_file.parent.mkdir(parents=True, exist_ok=True)

            x, y = click_position
            width, height = region_size

            left = max(0, x - width // 2)
            top = max(0, y - height // 2)

            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            screenshot.save(self.template_path)

            self._load_templates()

            return True

        except Exception as e:
            print(f"Warning: Could not save template: {e}")
            return False
