# Gemini Image Cleanup Audit

An offline pixel-difference checker, a four-case synthetic export dataset, and a practical acceptance checklist for visible Gemini watermark cleanup.

This repository helps answer a narrow question: did an image edit change dimensions or write pixels outside the expected corner? It is an evaluation utility, not a watermark remover. It makes no claim to detect or remove invisible SynthID watermarks, or to reconstruct original pixels perfectly.

## Run the checker

Python 3.10 or later and Pillow are required. Install the dependency with `python -m pip install -r requirements.txt`.

```sh
python pixel_audit.py flat-png.png flat-png-clean.png --box 944 688 48 48
```

For your own image pair, specify the actual edit rectangle in decoded pixel coordinates:

```sh
python pixel_audit.py original.png cleaned.png --box 944 688 48 48 --output audit.json
```

The command reports file bytes, dimensions, SHA-256 hashes, changed pixels inside/outside the rectangle, and a bounding box covering all changed pixels. Exit code 0 means dimensions matched and no decoded pixels changed outside the supplied rectangle; 1 means a dimension mismatch or outside change; 2 means invalid arguments or an unreadable file. A zero exit code is not an image-quality or authenticity certificate.

No network requests are made. Paths and image contents stay on the machine. The checker converts decoded images to RGBA without EXIF orientation transforms or ICC color-profile normalization. It compares decoded pixels, not metadata or compressed bytes. Use matching orientation and decoding workflows; large images may take longer because the checker scans each pixel.

## Included materials

- `measurements.csv`: the four originally published measurements, with source and configuration columns.
- `original-report.json`: the original experiment record, including input hashes and the tested engine hash.
- The four synthetic inputs and their four edited PNG outputs are stored at the repository root.
- `checklist.md`: a reusable before-publication acceptance checklist.
- `methodology.md`: measurement definitions, encoding settings, limitations, and exact ratio calculations.
- `verify_dataset.py`: rechecks the supplied fixture hashes and reported pixel/byte measurements.

```sh
python verify_dataset.py
```

The fixtures are programmatically generated flat shapes and texture, not real Gemini downloads. This small controlled dataset does not estimate success rates on real images, mobile performance, or an editor's overall quality. The original experiment used Pillow encoding, so browser exports can have different byte sizes. See the methodology before interpreting the values.

The accompanying explanation and browser tool are maintained at [WatermarkUndo](https://watermarkundo.com/gemini-watermark-remover-png-file-size).

## Reuse and contributions

The code, documentation, and synthetic fixtures contributed here are provided under the MIT license. Third-party product names and marks remain the property of their respective owners. No third-party removal engine, alpha-map source, analytics configuration, credentials, or private account files are included. Useful contributions include additional reproducible fixtures, documented decoding edge cases, and improvements to audit accuracy; promotional link-only submissions are not useful.
