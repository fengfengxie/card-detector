from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional, Tuple

import cv2
import numpy as np

from .detector import DetectionResult, DetectorConfig, detect_card, draw_detection, _resize_keep_aspect


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _clear_debug_dir(path: Path) -> None:
    for file_path in path.glob("*.png"):
        file_path.unlink()
    meta_path = path / "debug_meta.txt"
    if meta_path.exists():
        meta_path.unlink()


def generate_debug_images(
    image: np.ndarray,
    config: DetectorConfig,
    output_dir: Path,
) -> Tuple[Dict[str, str], Optional[DetectionResult]]:
    """Generate intermediate processing images for inspection.

    Returns a mapping of step name to file path.
    """
    _ensure_dir(output_dir)
    _clear_debug_dir(output_dir)

    resized, scale_factor = _resize_keep_aspect(image, config.max_side)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (config.blur_kernel, config.blur_kernel), 0)
    edges_canny = cv2.Canny(blur, config.canny_low, config.canny_high)
    edges_dilate = cv2.dilate(edges_canny, None, iterations=1)
    edges = cv2.erode(edges_dilate, None, iterations=1)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contour_vis = resized.copy()
    cv2.drawContours(contour_vis, contours, -1, (0, 128, 255), 2)

    outputs = {
        "01_resized": resized,
        "02_gray": gray,
        "03_blur": blur,
        "04_edges_canny": edges_canny,
        "05_edges_dilate": edges_dilate,
        "06_edges_erode": edges,
        "07_contours": contour_vis,
    }

    result = detect_card(image, config=config)
    if result is not None:
        annotated = draw_detection(image, result)
        outputs["08_detection"] = annotated

        resized_bbox = (np.array(result.bbox) * scale_factor).astype(np.int32)
        contour_best = resized.copy()
        cv2.polylines(contour_best, [resized_bbox], True, (0, 200, 0), 2)
        outputs["09_best_contour"] = contour_best

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
