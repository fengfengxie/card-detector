#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
DEFAULT_IMAGE_PATH="${ROOT_DIR}/input/11.jpg"
OUTPUT_DIR="${ROOT_DIR}/output"

if [[ $# -gt 1 ]]; then
  echo "Usage: $0 [image-path]"
  exit 1
fi

if [[ $# -eq 1 ]]; then
  if [[ "$1" = /* ]]; then
    IMAGE_PATH="$1"
  else
    IMAGE_PATH="${ROOT_DIR}/$1"
  fi
else
  IMAGE_PATH="${DEFAULT_IMAGE_PATH}"
fi

if [[ ! -f "${IMAGE_PATH}" ]]; then
  echo "Image not found: ${IMAGE_PATH}"
  exit 1
fi

if [[ ! -d "${VENV_DIR}" ]]; then
  python3 -m venv "${VENV_DIR}"
fi

"${VENV_DIR}/bin/pip" install -r "${ROOT_DIR}/requirements.txt" >/dev/null

mkdir -p "${OUTPUT_DIR}"

PYTHONPATH="${ROOT_DIR}/src" "${VENV_DIR}/bin/python" -m card_detector.cli \
  --image "${IMAGE_PATH}" \
  --output-json "${OUTPUT_DIR}/test.json" \
  --output-image "${OUTPUT_DIR}/test.png" \
  --debug-dir "${OUTPUT_DIR}/debug"

echo "Test completed. Outputs in ${OUTPUT_DIR}"
