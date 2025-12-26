"""
Configuration System
Centralized configuration and user preferences.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from ..visualization.theme_manager import Theme


class Config:
    """Manages application configuration and user preferences."""

    DEFAULT_CONFIG = {
        "theme": Theme.LIGHT.value,
        "animation": {
            "enabled": True,
            "speed": 1.0,
            "frames_per_step": 5,
            "curve": "ease_in_out",
        },
        "display": {
            "show_code_overlay": True,
            "show_variable_tracker": True,
            "show_performance_panel": True,
            "show_insights_panel": True,
            "font_size": 10,
        },
        "export": {
            "default_format": "png",
            "dpi": 300,
            "quality": "high",
        },
    }

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_file: Optional path to config file
        """
        self.config_file = config_file or self._get_default_config_path()
        self.config = self._load_config()

    def _get_default_config_path(self) -> str:
        """
        Get default config file path.

        Returns:
            Config file path
        """
        config_dir = Path.home() / ".ds_algo_lab"
        config_dir.mkdir(exist_ok=True)
        return str(config_dir / "config.json")

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file.

        Returns:
            Configuration dictionary
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    user_config = json.load(f)
                    # Merge with defaults
                    config = self.DEFAULT_CONFIG.copy()
                    self._merge_dict(config, user_config)
                    return config
            except Exception:
                # If loading fails, use defaults
                return self.DEFAULT_CONFIG.copy()
        return self.DEFAULT_CONFIG.copy()

    def _merge_dict(self, base: Dict[str, Any], update: Dict[str, Any]) -> None:
        """
        Recursively merge update dict into base dict.

        Args:
            base: Base dictionary
            update: Update dictionary
        """
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_dict(base[key], value)
            else:
                base[key] = value

    def save(self) -> None:
        """Save configuration to file."""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            key: Configuration key (supports dot notation, e.g., "animation.speed")
            default: Default value if not found

        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.

        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split(".")
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value

    def get_theme(self) -> Theme:
        """
        Get current theme.

        Returns:
            Theme enum value
        """
        theme_str = self.get("theme", Theme.LIGHT.value)
        try:
            return Theme(theme_str)
        except ValueError:
            return Theme.LIGHT

    def set_theme(self, theme: Theme) -> None:
        """
        Set theme.

        Args:
            theme: Theme to set
        """
        self.set("theme", theme.value)

    def get_animation_speed(self) -> float:
        """
        Get animation speed.

        Returns:
            Animation speed value
        """
        return self.get("animation.speed", 1.0)

    def set_animation_speed(self, speed: float) -> None:
        """
        Set animation speed.

        Args:
            speed: Animation speed
        """
        self.set("animation.speed", speed)

    def get_frames_per_step(self) -> int:
        """
        Get frames per step.

        Returns:
            Frames per step
        """
        return self.get("animation.frames_per_step", 5)

    def set_frames_per_step(self, frames: int) -> None:
        """
        Set frames per step.

        Args:
            frames: Number of frames per step
        """
        self.set("animation.frames_per_step", frames)

    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults."""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save()


# Global config instance
_global_config: Optional[Config] = None


def get_config() -> Config:
    """
    Get global configuration instance.

    Returns:
        Config instance
    """
    global _global_config
    if _global_config is None:
        _global_config = Config()
    return _global_config


def set_config(config: Config) -> None:
    """
    Set global configuration instance.

    Args:
        config: Config instance
    """
    global _global_config
    _global_config = config

