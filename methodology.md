# Measurement methods and limits

## Provenance

The measurements were made on 2026-10-18 and published in the [PNG file-size article](https://watermarkundo.com/gemini-watermark-remover-png-file-size). Inputs are our synthetic flat-color scene and textured scene; they are not original Gemini outputs. Input hashes and the original tested `app.js` hash are in `original-report.json`. The hash identifies the tested engine; the engine and its alpha map are not included in this repository.

The original engine experiment used a 1024 x 768 image, a 48 x 48 mark at x=944, y=688, strength 1.00, and texture seed 20261018. Input JPEGs used Pillow quality 85 and subsampling 2; PNGs used compression level 6. The original report records Pillow 12.3.0. Fixtures were copied byte-for-byte from that experiment and checked against its input hashes.

## Formulas and observed inputs

Byte ratio = output PNG bytes / input file bytes. The inputs below are measured file sizes from the included files, not estimates.

- flat PNG: 4611 / 5167 = 0.892394039 (published rounded ratio: 0.892).
- flat JPEG: 11263 / 19600 = 0.574642857 (published rounded ratio: 0.575).
- textured PNG: 1859900 / 1859915 = 0.999991935 (published rounded ratio: 1.0).
- textured JPEG: 1560060 / 225218 = 6.926888615 (published rounded ratio: 6.927).

Changed pixels = the number of locations where at least one decoded RGBA channel differs between before and after. Inside/outside use the supplied rectangle with inclusive left/top and exclusive right/bottom. Dimensions are decoded width and height, not file bytes. The original report's ratios are rounded to three decimal places; all other recorded counts and bytes are integers.

## Recheck, do not overclaim

`verify_dataset.py` recomputes bytes, dimensions, input hashes, and pixel counts against the supplied historical outputs. It does not rerun the original removal engine. In these fixtures every output retains the input dimensions, and no decoded pixels change outside the configured box. This does not prove perfect reconstruction, satisfactory visual quality, compatibility with all Gemini versions, or reliable handling of real JPEG screenshots.

Pillow PNG byte sizes are not predictions for browser PNG encoders. JPEG decoding is part of the input baseline; PNG export cannot recover detail already lost in JPEG compression. Neither script inspects invisible SynthID, authenticity, licensing rights, metadata retention, or mobile performance. For the browser API behind PNG export, see [MDN canvas.toBlob](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob).
