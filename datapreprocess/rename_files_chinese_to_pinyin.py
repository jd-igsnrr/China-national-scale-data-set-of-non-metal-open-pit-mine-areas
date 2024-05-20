from pathlib import Path
import pypinyin
import re

# Function to convert Chinese characters to pinyin
def chinese_to_pinyin(chinese_text):
    return ''.join(pypinyin.lazy_pinyin(chinese_text))

# Define the directory to search for files
base_dir = Path('.')

# Prepare a dictionary to keep track of Chinese text and their pinyin
chinese_pinyin_mapping = {}

# Iterate over all files in all subdirectories
for file_path in base_dir.rglob('*'):
    if file_path.is_file():
        # Extract the Chinese part using regex
        chinese_parts = re.findall(r'[\u4e00-\u9fff]+', file_path.stem)
        for chinese in chinese_parts:
            # Convert Chinese to pinyin
            pinyin = chinese_to_pinyin(chinese)
            # Replace the Chinese part with pinyin in the file name
            new_name = file_path.stem.replace(chinese, pinyin)
            # Save the mapping
            chinese_pinyin_mapping[chinese] = pinyin
            # Rename the file
            new_file_path = file_path.with_name(new_name).with_suffix(file_path.suffix)
            file_path.rename(new_file_path)
            # Optionally print the new file path (uncomment the next line to enable)
            # print(new_file_path)

# Save the Chinese text and their pinyin to a text file
with open('chinese_pinyin_mapping.txt', 'w', encoding='utf-8') as f:
    for chinese, pinyin in chinese_pinyin_mapping.items():
        f.write(f'{chinese} {pinyin}\n')