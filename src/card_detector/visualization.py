from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional, Tuple

import cv2
import numpy as np

from .detector import DetectionResult, DetectorConfig, detect_card, draw_detection, _resize_keep_aspect


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def generate_debug_images(
    image: np.ndarray,
    config: DetectorConfig,
    output_dir: Path,
) -> Tuple[Dict[str, str], Optional[DetectionResult]]:
    """Generate intermediate processing images for inspection.

    Returns a mapping of step name to file path.
    """
    _ensure_dir(output_dir)

    resized, scale_factor = _resize_keep_aspect(image, config.max_side)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (config.blur_kernel, config.blur_kernel), 0)
    edges_canny = cv2.Canny(blur, config.canny_low, config.canny_high)
    edges_dilate = cv2.dilate(edges_canny, None, iterations=1)
    edges = cv2.erode(edges_dilate, None, iterations=1)

    outputs = {
        "01_resized": resized,
        "02_gray": gray,
        "03_blur": blur,
        "04_edges_canny": edges_canny,
        "05_edges_dilate": edges_dilate,
        "06_edges": edges,
    }

    result = detect_card(image, config=config)
    if result is not None:
        annotated = draw_detection(image, result)
        outputs["07_detection"] = annotated

    paths: Dict[str, str] = {}
    for name, data in outputs.items():
        if data.ndim == 2:
            save_img = cv2.cvtColor(data, cv2.COLOR_GRAY2BGR)
        else:
            save_img = data
        filename = output_dir / f"{name}.png"
        cv2.imwrite(str(filename), save_img)
        paths[name] = str(filename)

    meta_path = output_dir / "debug_meta.txt"
    meta_path.write_text(
        f"scale_factor={scale_factor}\n"
        f"max_side={config.max_side}\n"
        f"blur_kernel={config.blur_kernel}\n"
        f"canny_low={config.canny_low}\n"
        f"canny_high={config.canny_high}\n",
        encoding="utf-8",
    )

    return paths, result
