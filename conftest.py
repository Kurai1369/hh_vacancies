"""Глобальные фикстуры и настройки pytest"""

import sys
from pathlib import Path

# Добавляем src в sys.path для импортов
sys.path.insert(0, str(Path(__file__).parent / "src"))
