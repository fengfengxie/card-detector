# Card Detector

Detect a standard ID-1 card (ISO/IEC 7810) in a single image using classic OpenCV
geometry. The tool outputs a bounding box, confidence score, and pixel-to-mm
scale to support downstream measurement workflows.

## Features
- Single-card detection in simple backgrounds
- Rotated bounding box from `minAreaRect`
- `bbox`, `confidence`, and `scale` outputs in JSON
- Optional annotated output image and debug visualizations

## Requirements
- Python 3.x
- OpenCV (`opencv-python`)
- NumPy

See `requirements.txt` for the full dependency list.

## Quick Start
1. Create a virtual environment and install dependencies.
2. Run the CLI against an input image.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
PYTHONPATH=src .venv/bin/python -m card_detector.cli \
  --image input/11.jpg \
  --output-json output/result.json \
  --output-image output/result.png \
  --debug-dir output/debug
```

## CLI Usage
```bash
PYTHONPATH=src python -m card_detector.cli --image path/to/image.jpg [options]
```

Options:
- `--output-json`: Save JSON result to file (prints to stdout if omitted)
- `--output-image`: Save annotated image
- `--debug-dir`: Save intermediate debug images
- `--max-side`: Max side length for processing (default: `1200`)
- `--canny-low`: Canny low threshold (default: `50`)
- `--canny-high`: Canny high threshold (default: `150`)

## Output Format
Example JSON structure:
```json
{
  "bbox": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],
  "confidence": 0.87,
  "scale": {
    "px_per_mm": 7.42,
    "mm_per_px": 0.13
  },
  "meta": {
    "image_size": { "width": 4032, "height": 3024 },
    "processing_time_sec": 0.15,
    "scale_factor": 0.30,
    "params": { "...": "..." }
  }
}
```

## Project Structure
- `src/`: application code
- `script/`: build/test scripts
- `doc/`: PRD/Plan/Progress and project notes
- `input/`: sample inputs
- `output/`: generated outputs

## Scripts
- `script/build.sh`: placeholder build script
- `script/test.sh`: runs the CLI on `input/11.jpg` and writes to `output/`

## Docs
Project planning docs live in `doc/v1.0/`:
- `doc/v1.0/PRD.md`
- `doc/v1.0/Plan.md`
- `doc/v1.0/Progress.md`

## License
See `LICENSE`.
