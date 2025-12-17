#!/usr/bin/env python3
"""
Convert CSV annotations to COCO format for Orange Leaf Disease Classification dataset.
"""

import os
import json
import csv
import argparse
from pathlib import Path
from PIL import Image
import random

def load_labelmap(labelmap_path):
    """Load labelmap.json"""
    with open(labelmap_path, 'r', encoding='utf-8') as f:
        labelmap = json.load(f)
    return {item['object_id']: item['object_name'] for item in labelmap}

def parse_csv(csv_path):
    """Parse CSV annotation file"""
    annotations = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip comment lines
            if row.get('#item', '').startswith('#'):
                continue
            try:
                item = int(row.get('#item', 0))
                x = float(row.get('x', 0))
                y = float(row.get('y', 0))
                width = float(row.get('width', row.get('w', row.get('dx', 0))))
                height = float(row.get('height', row.get('h', row.get('dy', 0))))
                label = int(row.get('label', row.get('class', row.get('category_id', 1))))
                annotations.append({
                    'item': item,
                    'bbox': [x, y, width, height],
                    'label': label
                })
            except (ValueError, KeyError) as e:
                continue
    return annotations

def get_image_info(image_path):
    """Get image dimensions"""
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception:
        return (512, 512)  # Default

def convert_to_coco(root_dir, output_dir, categories=None, splits=None, combined=False):
    """Convert CSV annotations to COCO format"""
    root = Path(root_dir)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    
    if categories is None:
        categories = ['healthy_leaf', 'citrus_canker', 'citrus_greening', 'yellow_dragon', 
                     'powdery_mildew', 'shot_hole', 'die_back', 'citrus_mealybugs', 
                     'spiny_whitefly', 'yellow_leaves', 'foliage_damaged']
    if splits is None:
        splits = ['train', 'val', 'test']
    
    # Load labelmap
    labelmap_path = root / 'oranges' / 'labelmap.json'
    labelmap = load_labelmap(labelmap_path)
    
    # Build category list from labelmap
    coco_categories = []
    for obj_id, obj_name in sorted(labelmap.items()):
        if obj_id == 0:
            coco_categories.append({
                'id': 0,
                'name': 'background',
                'supercategory': 'background'
            })
        else:
            coco_categories.append({
                'id': obj_id,
                'name': obj_name,
                'supercategory': 'orange_leaf'
            })
    
    # Process each category and split
    all_coco_data = {}
    
    for split in splits:
        # Process each category
        for category in categories:
            category_dir = root / 'oranges' / category
            images_dir = category_dir / 'images'
            csv_dir = category_dir / 'csv'
            sets_dir = category_dir / 'sets'
            
            if not images_dir.exists():
                print(f"Warning: {images_dir} does not exist, skipping {category}")
                continue
            
            # Load split file for this category
            split_file = sets_dir / f'{split}.txt'
            split_images = set()
            if split_file.exists():
                with open(split_file, 'r', encoding='utf-8') as f:
                    split_images = {line.strip() for line in f if line.strip()}
                print(f"Loaded {len(split_images)} images for {category}/{split} split")
            else:
                print(f"Warning: Split file '{split_file}' does not exist, using all images")
            
            coco_data = {
                'info': {
                    'year': 2025,
                    'version': '1.0',
                    'description': f'Orange Leaf Disease Classification {category} {split} split',
                    'url': ''
                },
                'images': [],
                'annotations': [],
                'categories': coco_categories,
                'licenses': []
            }
            
            # Get images in this split
            if split_images:
                image_files = []
                for stem in split_images:
                    for ext in ['.jpg', '.png', '.jpeg', '.bmp']:
                        img_path = images_dir / f"{stem}{ext}"
                        if img_path.exists():
                            image_files.append(img_path)
                            break
            else:
                # If split file doesn't exist, use all images
                image_files = list(images_dir.glob('*.jpg'))
                image_files.extend(images_dir.glob('*.png'))
                image_files.extend(images_dir.glob('*.jpeg'))
                image_files.extend(images_dir.glob('*.bmp'))
            
            # Process images
            image_id_map = {}
            annotation_id = 1
            
            for img_path in image_files:
                stem = img_path.stem
                
                # Check if in split (already filtered above, but double-check)
                if split_images and stem not in split_images:
                    continue
                
                # Get image info
                width, height = get_image_info(img_path)
                image_id = random.randint(1000000000, 9999999999)
                image_id_map[stem] = image_id
                
                coco_data['images'].append({
                    'id': image_id,
                    'file_name': f'oranges/{category}/images/{img_path.name}',
                    'width': width,
                    'height': height
                })
                
                # Load CSV annotations
                csv_path = csv_dir / f'{stem}.csv'
                if csv_path.exists():
                    annotations = parse_csv(csv_path)
                    for ann in annotations:
                        bbox = ann['bbox']
                        category_id = ann['label']
                        
                        coco_data['annotations'].append({
                            'id': annotation_id,
                            'image_id': image_id,
                            'category_id': category_id,
                            'bbox': bbox,
                            'area': bbox[2] * bbox[3],
                            'iscrowd': 0
                        })
                        annotation_id += 1
            
            # Save single category file
            output_file = output / f'{category}_instances_{split}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(coco_data, f, indent=2, ensure_ascii=False)
            print(f"Created {output_file}: {len(coco_data['images'])} images, {len(coco_data['annotations'])} annotations")
            
            if split not in all_coco_data:
                all_coco_data[split] = {
                    'info': {
                        'year': 2025,
                        'version': '1.0',
                        'description': f'Orange Leaf Disease Classification combined {split} split',
                        'url': ''
                    },
                    'images': [],
                    'annotations': [],
                    'categories': coco_categories,
                    'licenses': []
                }
            
            # Add to combined data
            all_coco_data[split]['images'].extend(coco_data['images'])
            all_coco_data[split]['annotations'].extend(coco_data['annotations'])
    
    # Create combined files if requested
    if combined:
        for split in splits:
            if split in all_coco_data:
                output_file = output / f'combined_instances_{split}.json'
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(all_coco_data[split], f, indent=2, ensure_ascii=False)
                print(f"Created {output_file}: {len(all_coco_data[split]['images'])} images, {len(all_coco_data[split]['annotations'])} annotations")

def main():
    parser = argparse.ArgumentParser(description='Convert CSV annotations to COCO format')
    parser.add_argument('--root', type=str, default='.', help='Dataset root directory')
    parser.add_argument('--out', type=str, default='annotations', help='Output directory')
    parser.add_argument('--categories', nargs='+', 
                        default=['healthy_leaf', 'citrus_canker', 'citrus_greening', 'yellow_dragon', 
                                'powdery_mildew', 'shot_hole', 'die_back', 'citrus_mealybugs', 
                                'spiny_whitefly', 'yellow_leaves', 'foliage_damaged'],
                        help='Categories to process')
    parser.add_argument('--splits', nargs='+', default=['train', 'val', 'test'], help='Splits to process')
    parser.add_argument('--combined', action='store_true', help='Create combined COCO files')
    
    args = parser.parse_args()
    convert_to_coco(args.root, args.out, args.categories, args.splits, args.combined)

if __name__ == '__main__':
    main()

