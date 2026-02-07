from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import cv2

from .detector import DetectorConfig, detect_card, draw_detection
from .visualization import generate_debug_images


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect a standard ID-1 card in an image.")
    parser.add_argument("--image", required=True, help="Path to input image")
    parser.add_argument("--output-json", help="Path to save JSON result")
    parser.add_argument("--output-image", help="Path to save annotated image")
    parser.add_argument("--debug-dir", help="Directory to save debug images")
    parser.add_argument("--max-side", type=int, default=1200, help="Max side length for processing")
    parser.add_argument("--canny-low", type=int, default=50, help="Canny low threshold")
    parser.add_argument("--canny-high", type=int, default=150, help="Canny high threshold")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    image_path = Path(args.image)
    if not image_path.exists():
        print(f"Image not found: {image_path}", file=sys.stderr)
        return 1

    image = cv2.imread(str(image_path))
    if image is None:
        print(f"Failed to read image: {image_path}", file=sys.stderr)
        return 1

    config = DetectorConfig(max_side=args.max_side, canny_low=args.canny_low, canny_high=args.canny_high)
    result = detect_card(image, config=config)

    if result is None:
        print("No card detected.", file=sys.stderr)
        return 2

    output = {
        "bbox": result.bbox,
        "confidence": result.confidence,
        "scale": result.scale,
        "meta": result.meta,
    }

    if args.output_json:
        output_path = Path(args.output_json)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    else:
        print(json.dumps(output, indent=2))

    if args.output_image:
        output_image = draw_detection(image, result)
        output_path = Path(args.output_image)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output_path), output_image)

    if args.debug_dir:
        debug_dir = Path(args.debug_dir)
        generate_debug_images(image, config=config, output_dir=debug_dir)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
