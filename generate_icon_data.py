"""Generate base64 encoded SVG icons for embedding."""
import base64
import os

icons_dir = 'custom_components/varsom/icons'

print("# Base64 encoded Yr.no warning icons\n")
print("ICON_DATA_URLS = {")

for filename in sorted(os.listdir(icons_dir)):
    if filename.endswith('.svg'):
        with open(os.path.join(icons_dir, filename), 'rb') as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
            icon_key = filename.replace('.svg', '').replace('icon-warning-', '')
            print(f'    "{icon_key}": "data:image/svg+xml;base64,{encoded}",')

print("}")
