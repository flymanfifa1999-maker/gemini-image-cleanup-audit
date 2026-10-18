"""Recheck supplied historical measurements; does not run a removal engine."""
import json
from pathlib import Path
from pixel_audit import inspect_pair

def main():
    root=Path(__file__).resolve().parent
    report=json.loads((root/'original-report.json').read_text(encoding='utf-8'))
    checked=[]
    for item in report['results']:
        name=item['scene']+'-'+item['input_format'].lower()
        before=root/(name+('.jpg' if item['input_format']=='JPEG' else '.png'))
        after=root/(name+'-clean.png')
        pos=report['position']
        actual=inspect_pair(before,after,(pos['x'],pos['y'],pos['size'],pos['size']))
        comparisons={
            'before_bytes':item['input_bytes'],'after_bytes':item['output_png_bytes'],
            'before_dimensions':[item['width'],item['height']],
            'after_dimensions':[item['width'],item['height']],
            'before_sha256':item['input_sha256'],
            'changed_pixels_inside':item['inside_box_changed_pixels'],
            'changed_pixels_outside':item['outside_box_changed_pixels'],
        }
        for key,expected in comparisons.items():
            if actual[key] != expected: raise ValueError(f'{name}: {key} differs: {actual[key]} != {expected}')
        if round(actual['byte_ratio'],3) != item['ratio']: raise ValueError(f'{name}: rounded ratio differs')
        checked.append({'case':name,'bytes_and_pixels_match_original_report':True})
    print(json.dumps({'verified_cases':len(checked),'results':checked},indent=2))

if __name__ == '__main__': main()
