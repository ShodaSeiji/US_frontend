import zipfile
import os

# 除外対象
exclude_dirs = ['.git', '.vscode', '__pycache__']
exclude_exts = ['.pyc', '.pkl']
max_file_size = 1024 * 1024 * 100  # 100MB制限
output_zip = 'us_frontend_deploy.zip'

with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
    for root, dirs, files in os.walk('.'):
        if any(ex in root for ex in exclude_dirs):
            continue
        for file in files:
            filepath = os.path.join(root, file)

            # 🛑 zip自身を含めない
            if os.path.abspath(filepath) == os.path.abspath(output_zip):
                continue

            if any(file.endswith(ext) for ext in exclude_exts):
                continue
            try:
                if os.path.getsize(filepath) > max_file_size:
                    print(f"⚠ Skipping large file: {filepath}")
                    continue
                arcname = os.path.relpath(filepath, '.')
                zipf.write(filepath, arcname)
            except Exception as e:
                print(f"❌ Failed to add {filepath}: {e}")
