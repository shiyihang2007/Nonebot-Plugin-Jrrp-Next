from pathlib import Path

resource_root = Path(__file__).parent.absolute() / "resource"
resource_root.mkdir(exist_ok=True, parents=True)


class StaticPath:
    # Font
    AlibabaPuHuiTi = resource_root / "font" / "AlibabaPuHuiTi-ExtraBold.ttf"
    DengXian = resource_root / "font" / "Deng.ttf"
    Aldrich = resource_root / "font" / "Aldrich-Regular.ttf"
