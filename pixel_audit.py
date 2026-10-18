"""Compare decoded pixels before/after an edit; no uploads or watermark removal."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

def inspect_pair(before_path, after_path, box):
    before_path, after_path = Path(before_path), Path(after_path)
    with Image.open(before_path) as im:
        before_format, before_size = im.format, im.size
        before = im.convert('RGBA')
    with Image.open(after_path) as im:
        after_format, after_size = im.format, im.size
        after = im.convert('RGBA')
    x, y, width, height = box
    if min(x, y) < 0 or min(width, height) <= 0:
        raise ValueError('Box requires nonnegative x/y and positive width/height.')
    if x + width > before.width or y + height > before.height:
        raise ValueError('Box extends beyond the input image.')
    result = {
        'before_name': before_path.name, 'after_name': after_path.name,
        'before_format': before_format, 'after_format': after_format,
        'before_dimensions': list(before_size), 'after_dimensions': list(after_size),
        'before_bytes': before_path.stat().st_size, 'after_bytes': after_path.stat().st_size,
        'byte_ratio': after_path.stat().st_size / before_path.stat().st_size,
        'byte_ratio_formula': 'after_bytes / before_bytes',
        'dimensions_equal': before_size == after_size, 'box_xywh': list(box),
        'before_sha256': hashlib.sha256(before_path.read_bytes()).hexdigest(),
        'after_sha256': hashlib.sha256(after_path.read_bytes()).hexdigest(),
    }
    if before_size != after_size:
        result.update(changed_pixels_inside=None, changed_pixels_outside=None,
                      note='Pixel locations are not comparable when dimensions differ.')
        return result
    inside = outside = 0
    left, top, right, bottom = before.width, before.height, -1, -1
    raw_a, raw_b = before.tobytes(), after.tobytes()
    for pos in range(0, len(raw_a), 4):
        if raw_a[pos:pos+4] == raw_b[pos:pos+4]: continue
        pixel = pos // 4; px, py = pixel % before.width, pixel // before.width
        if x <= px < x + width and y <= py < y + height: inside += 1
        else: outside += 1
        left, top, right, bottom = min(left,px), min(top,py), max(right,px), max(bottom,py)
    result.update(changed_pixels_inside=inside, changed_pixels_outside=outside,
                  changed_bbox_xywh=None if right < 0 else [left,top,right-left+1,bottom-top+1],
                  note='Decoded RGBA equality only; not a restoration score or SynthID test. No EXIF orientation transform or color-profile normalization is applied.')
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before'); parser.add_argument('after')
    parser.add_argument('--box',type=int,nargs=4,metavar=('X','Y','WIDTH','HEIGHT'),required=True)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    try: result=inspect_pair(args.before,args.after,args.box)
    except (OSError,ValueError) as error: parser.exit(2,str(error)+'\n')
    text=json.dumps(result,indent=2)
    if args.output: args.output.write_text(text+'\n',encoding='utf-8')
    print(text)
    return 1 if not result['dimensions_equal'] or result['changed_pixels_outside'] else 0

if __name__ == '__main__': raise SystemExit(main())
