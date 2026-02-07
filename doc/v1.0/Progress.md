# Progress

## Phase 1: Minimum Viable Detection
- [x] Read image and basic preprocessing (resize, blur, grayscale)
- [x] Edge detection and contour extraction
- [x] Contour filtering by area, aspect ratio, and rectangularity
- [x] Output bbox and basic confidence score
- [x] CLI output JSON and annotated image

## Phase 2: Accuracy & Robustness
- [ ] Perspective correction and refined four-point fitting
- [ ] Adaptive thresholding for lighting variation
- [ ] Confidence scoring based on geometric consistency and edge clarity

## Phase 3: Calibration & Evaluation
- [x] Pixel-to-mm scale calculation using ISO/IEC 7810 ID-1 dimensions
- [ ] Evaluation script and error statistics
- [ ] Test report generation

## Notes
- Current detector targets single-card, simple-background images.
