"""Copy the maintained registry directory into the installable CLI package."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "registries" / "sources.json"
destination = ROOT / "markscout" / "data" / "sources.json"
shutil.copyfile(source, destination)
print(f"Updated {destination.relative_to(ROOT)} from {source.relative_to(ROOT)}")
