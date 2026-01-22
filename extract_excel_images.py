#!/usr/bin/env python3
import sys
import json
import base64
import tempfile
import os

try:
    from openpyxl import load_workbook
except ImportError:
    print(json.dumps({'success': False, 'error': 'openpyxl not installed'}))
    sys.exit(1)

def extract_images(excel_base64):
    excel_data = base64.b64decode(excel_base64)
    temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
    temp_file.write(excel_data)
    temp_file.close()
    
    try:
        wb = load_workbook(temp_file.name)
        ws = wb.active
        
        images_data = []
        for idx, image in enumerate(ws._images):
            anchor = image.anchor
            row = anchor._from.row if hasattr(anchor, '_from') else idx
            product_index = (row - 1) // 8
            
            image_bytes = image._data()
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            if hasattr(image, 'format'):
                ext = image.format.lower()
            elif hasattr(image, 'path') and image.path:
                ext = image.path.split('.')[-1].lower()
            else:
                ext = 'png'
            
            images_data.append({
                'productIndex': product_index + 1,
                'row': row,
                'filename': f'product_{product_index + 1}_image_{idx + 1}.{ext}',
                'mimeType': f'image/{ext}',
                'base64': image_base64
            })
        
        return {'success': True, 'images': images_data, 'count': len(images_data)}
    except Exception as e:
        return {'success': False, 'error': str(e)}
    finally:
        os.unlink(temp_file.name)

if __name__ == '__main__':
    excel_base64 = sys.stdin.read().strip()
    result = extract_images(excel_base64)
    print(json.dumps(result))