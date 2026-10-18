# Image cleanup acceptance checklist

1. Keep the original; save the edited image under a different filename.
2. Compare width and height. A larger PNG is not evidence of an upscale.
3. Record input/output formats and byte sizes. Compute byte ratio as output bytes divided by input bytes; do not call that ratio an image-quality score.
4. Specify the actual edited rectangle. Run `pixel_audit.py` to check whether decoded pixels changed outside it.
5. At the same zoom, inspect the edited corner for a remaining sparkle, dark halo, broken line, damaged lettering, or interrupted texture.
6. Inspect an unchanged control crop away from the edit. An automated count complements this visual check; it does not replace it.
7. Keep a PNG master if it suits your workflow. If you create a smaller sharing copy, inspect that separately because lossy encoding can change pixels throughout the image.
8. Record tool version, settings, image source, and failures. Never label a synthetic fixture as a real Gemini output.
9. State the boundary: this check concerns visible edits and decoded pixels. It neither detects nor removes SynthID and does not certify provenance.
