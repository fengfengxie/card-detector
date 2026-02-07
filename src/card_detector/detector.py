from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np

CARD_LONG_MM = 85.60
CARD_SHORT_MM = 53.98
CARD_ASPECT = CARD_LONG_MM / CARD_SHORT_MM


@dataclass
class DetectionResult:
    bbox: List[List[float]]
    confidence: float
    scale: Dict[str, float]
    meta: Dict[str, Any]


@dataclass
class DetectorConfig:
    max_side: int = 1200
    blur_kernel: int = 5
    canny_low: int = 50
    canny_high: int = 150
    min_area_ratio: float = 0.05
    max_area_ratio: float = 0.95
    approx_epsilon_ratio: float = 0.02
    rectangularity_weight: float = 0.55
    aspect_weight: float = 0.45


def _resize_keep_aspect(image: np.ndarray, max_side: int) -> Tuple[np.ndarray, float]:
    height, width = image.shape[:2]
    max_dim = max(height, width)
    if max_dim <= max_side:
        return image, 1.0
    scale = max_side / max_dim
    resized = cv2.resize(image, (int(width * scale), int(height * scale)))
    return resized, scale


def _order_points_clockwise(points: np.ndarray) -> np.ndarray:
    center = points.mean(axis=0)
    angles = np.arctan2(points[:, 1] - center[1], points[:, 0] - center[0])
    sort_idx = np.argsort(angles)
    return points[sort_idx]


def _score_candidate(box: np.ndarray, contour: np.ndarray, image_area: float, config: DetectorConfig) -> float:
    rect_area = cv2.contourArea(box)
    contour_area = cv2.contourArea(contour)
    if rect_area <= 0 or contour_area <= 0:
        return 0.0

    rectangularity = max(0.0, min(1.0, contour_area / rect_area))
    width = np.linalg.norm(box[0] - box[1])
    height = np.linalg.norm(box[1] - box[2])
    if height <= 0 or width <= 0:
        return 0.0

    aspect = max(width, height) / min(width, height)
    aspect_score = 1.0 - min(1.0, abs(aspect - CARD_ASPECT) / CARD_ASPECT)
    area_ratio = rect_area / image_area
    if not (config.min_area_ratio <= area_ratio <= config.max_area_ratio):
        return 0.0

    return rectangularity * config.rectangularity_weight + aspect_score * config.aspect_weight


def detect_card(image: np.ndarray, config: Optional[DetectorConfig] = None) -> Optional[DetectionResult]:
    if config is None:
        config = DetectorConfig()

    start = time.time()
    resized, scale_factor = _resize_keep_aspect(image, config.max_side)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (config.blur_kernel, config.blur_kernel), 0)
    edges = cv2.Canny(blur, config.canny_low, config.canny_high)
    edges = cv2.dilate(edges, None, iterations=1)
    edges = cv2.erode(edges, None, iterations=1)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    image_area = float(resized.shape[0] * resized.shape[1])

    best_score = 0.0
    best_box = None
    best_contour = None

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, config.approx_epsilon_ratio * perimeter, True)
        if len(approx) < 4:
            continue
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        score = _score_candidate(box, contour, image_area, config)
        if score > best_score:
            best_score = score
            best_box = box
            best_contour = contour

    if best_box is None or best_contour is None:
        return None

    ordered_box = _order_points_clockwise(best_box)
    ordered_box = ordered_box / scale_factor

    width = np.linalg.norm(ordered_box[0] - ordered_box[1])
    height = np.linalg.norm(ordered_box[1] - ordered_box[2])
    long_px = max(width, height)
    short_px = min(width, height)

    px_per_mm_long = long_px / CARD_LONG_MM
    px_per_mm_short = short_px / CARD_SHORT_MM
    px_per_mm = (px_per_mm_long + px_per_mm_short) / 2.0

    elapsed = time.time() - start

    result = DetectionResult(
        bbox=ordered_box.tolist(),
        confidence=float(min(1.0, best_score)),
        scale={
            "px_per_mm": float(px_per_mm),
            "mm_per_px": float(1.0 / px_per_mm) if px_per_mm > 0 else 0.0,
        },
        meta={
            "image_size": {"width": int(image.shape[1]), "height": int(image.shape[0])},
            "processing_time_sec": float(elapsed),
            "scale_factor": float(scale_factor),
            "params": {
                "max_side": config.max_side,
                "blur_kernel": config.blur_kernel,
                "canny_low": config.canny_low,
                "canny_high": config.canny_high,
                "min_area_ratio": config.min_area_ratio,
                "max_area_ratio": config.max_area_ratio,
                "approx_epsilon_ratio": config.approx_epsilon_ratio,
            },
        },
    )

    return result


def draw_detection(image: np.ndarray, result: DetectionResult) -> np.ndarray:
    output = image.copy()
    pts = np.array(result.bbox, dtype=np.int32)
    cv2.polylines(output, [pts], True, (0, 200, 0), 2)
    label = f"conf={result.confidence:.2f}, px/mm={result.scale['px_per_mm']:.2f}"
    cv2.putText(output, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 0), 2)
    return output
