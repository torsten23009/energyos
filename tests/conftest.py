"""Import EnergyOS pure modules without requiring Home Assistant installed."""
import sys
import types
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "custom_components" / "energyos"
package = types.ModuleType("energyos")
package.__path__ = [str(root)]
sys.modules["energyos"] = package
