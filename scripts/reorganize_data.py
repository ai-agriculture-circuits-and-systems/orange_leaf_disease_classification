#!/usr/bin/env python3
"""
Reorganize orange leaf disease classification dataset to standard structure.
"""

import os
import shutil
import json
import re
import random
from pathlib import Path
from PIL import Image

# Mapping from original folder names to standard subcategory names
FOLDER_MAPPING = {
    'Healthy leaf': 'healthy_leaf',
    'Citrus canker': 'citrus_canker',
    'Citrus greening': 'citrus_greening',
    'Yellow dragon': 'yellow_dragon',
    'Powdery mildew': 'powdery_mildew',
    'Shot hole': 'shot_hole',
    'Die back': 'die_back',
    'Citrus mealybugs': 'citrus_mealybugs',
    'Spiny whitefly': 'spiny_whitefly',
    'Yellow leaves': 'yellow_leaves',
    'Foliage damaged': 'foliage_damaged'
}

# Category ID mapping (from labelmap.json)
CATEGORY_ID_MAPPING = {
    'healthy_leaf': 1,
    'citrus_canker': 2,
    'citrus_greening': 3,
    'yellow_dragon': 4,
    'powdery_mildew': 5,
    'shot_hole': 6,
    'die_back': 7,
    'citrus_mealybugs': 8,
    'spiny_whitefly': 9,
    'yellow_leaves': 10,
    'foliage_damaged': 11
}

def normalize_disease_name(disease_name):
    """Convert disease name to annotation format"""
    mapping = {
        'Citrus greening': 'Citrus_greening',
        'Yellow dragon': 'Yellow_dragon',
        'Powdery mildew': 'Powdery_mildew',
        'Shot hole': 'Shot_hole',
        'Die back': 'Die_back',
        'Citrus canker': 'Citrus_canker',
        'Citrus mealybugs': 'Citrus_mealybugs',
        'Spiny whitefly': 'Spiny_whitefly',
        'Foliage damaged': 'Foliage_damaged',
        'Yellow leaves': 'Yellow_leaves',
        'Healthy leaf': 'Healthy_leaf'
    }
    return mapping.get(disease_name, disease_name.replace(' ', '_'))

def extract_number_from_filename(filename):
    """Extract number from filename like 'Citrus Greening3.jpeg' -> 3"""
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else None

def find_matching_annotation(image_filename, disease_name, annotation_dir):
    """Find matching annotation file based on naming pattern"""
    number = extract_number_from_filename(image_filename)
    if number is None:
        return None
    
    normalized_disease = normalize_disease_name(disease_name)
    possible_names = [
        f"{normalized_disease} ({number}).txt",
        f"{normalized_disease} ({number}).jpg"
    ]
    
    for name in possible_names:
        annotation_path = os.path.join(annotation_dir, name)
        if os.path.exists(annotation_path):
            return annotation_path
    
    return None

def parse_yolo_annotation(annotation_path, img_width, img_height):
    """Parse YOLO format annotation and convert to CSV format"""
    annotations = []
    if os.path.exists(annotation_path):
        try:
            with open(annotation_path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        category_id = int(parts[0])
                        x_center = float(parts[1])
                        y_center = float(parts[2])
                        width = float(parts[3])
                        height = float(parts[4])
                        
                        # Convert normalized coordinates to pixel coordinates
                        x = (x_center - width/2) * img_width
                        y = (y_center - height/2) * img_height
                        w = width * img_width
                        h = height * img_height
                        
                        annotations.append({
                            'item': len(annotations),
                            'x': x,
                            'y': y,
                            'width': w,
                            'height': h,
                            'label': category_id + 1  # YOLO uses 0-based, we use 1-based
                        })
        except Exception as e:
            print(f"Error parsing annotation file {annotation_path}: {e}")
    
    return annotations

def convert_to_csv(annotations):
    """Convert annotations to CSV format"""
    if not annotations:
        return "#item,x,y,width,height,label\n"
    
    lines = ["#item,x,y,width,height,label"]
    for ann in annotations:
        lines.append(f"{ann['item']},{ann['x']:.2f},{ann['y']:.2f},{ann['width']:.2f},{ann['height']:.2f},{ann['label']}")
    
    return "\n".join(lines) + "\n"

def update_json_annotation(json_path, category_name, category_id):
    """Update JSON annotation file with correct category information"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Update category information
        if 'categories' in data and len(data['categories']) > 0:
            data['categories'][0]['id'] = category_id
            data['categories'][0]['name'] = category_name.replace('_', ' ').title()
            data['categories'][0]['supercategory'] = "orange_leaf"
        
        # Update annotations category_id
        if 'annotations' in data:
            for ann in data['annotations']:
                ann['category_id'] = category_id
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error updating JSON annotation {json_path}: {e}")

def reorganize_dataset(root_dir):
    """Reorganize dataset to standard structure"""
    root = Path(root_dir)
    converted_dir = root / "Converted Image"
    annotation_dir = root / "Annotation"
    oranges_dir = root / "oranges"
    
    if not converted_dir.exists():
        print(f"Error: {converted_dir} does not exist")
        return
    
    all_images = []
    
    # Process each category folder
    for orig_folder_name, subcategory in FOLDER_MAPPING.items():
        orig_folder = converted_dir / orig_folder_name
        if not orig_folder.exists():
            print(f"Warning: {orig_folder} does not exist, skipping...")
            continue
        
        print(f"Processing {orig_folder_name} -> {subcategory}...")
        
        # Create subcategory directories
        subcategory_dir = oranges_dir / subcategory
        images_dir = subcategory_dir / "images"
        csv_dir = subcategory_dir / "csv"
        json_dir = subcategory_dir / "json"
        
        images_dir.mkdir(parents=True, exist_ok=True)
        csv_dir.mkdir(parents=True, exist_ok=True)
        json_dir.mkdir(parents=True, exist_ok=True)
        
        category_id = CATEGORY_ID_MAPPING[subcategory]
        
        # Process images
        for image_file in sorted(orig_folder.glob("*.jpeg")):
            if image_file.suffix.lower() not in ['.jpg', '.jpeg', '.png']:
                continue
            
            # Get image dimensions
            try:
                img = Image.open(image_file)
                img_width, img_height = img.size
            except Exception as e:
                print(f"Error reading image {image_file}: {e}")
                continue
            
            # Generate new filename (remove 'Con_' prefix if present)
            stem = image_file.stem
            if stem.startswith('Con_'):
                stem = stem[4:]
            new_filename = f"{stem}{image_file.suffix}"
            
            # Copy image
            dest_image = images_dir / new_filename
            shutil.copy2(image_file, dest_image)
            
            # Find matching annotation
            annotation_path = find_matching_annotation(image_file.name, orig_folder_name, annotation_dir)
            
            # Create CSV annotation
            if annotation_path:
                annotations = parse_yolo_annotation(annotation_path, img_width, img_height)
            else:
                # Default: full image annotation for classification task
                annotations = [{
                    'item': 0,
                    'x': 0.0,
                    'y': 0.0,
                    'width': float(img_width),
                    'height': float(img_height),
                    'label': category_id
                }]
            
            csv_content = convert_to_csv(annotations)
            csv_file = csv_dir / f"{stem}.csv"
            with open(csv_file, 'w', encoding='utf-8') as f:
                f.write(csv_content)
            
            # Copy/update JSON annotation
            json_file_orig = orig_folder / f"{image_file.stem}.json"
            json_file_dest = json_dir / f"{stem}.json"
            
            if json_file_orig.exists():
                shutil.copy2(json_file_orig, json_file_dest)
                update_json_annotation(json_file_dest, subcategory, category_id)
            else:
                # Create new JSON annotation
                create_json_annotation(json_file_dest, new_filename, img_width, img_height, 
                                     subcategory, category_id, annotations)
            
            all_images.append((subcategory, stem))
            
            print(f"  Processed: {new_filename}")
    
    print(f"\nTotal images processed: {len(all_images)}")
    
    # Create dataset splits
    create_dataset_splits(oranges_dir, all_images)

def create_json_annotation(json_path, filename, width, height, category_name, category_id, annotations):
    """Create a new JSON annotation file"""
    import random
    import time
    
    def generate_unique_id():
        random_part = random.randint(1000000000, 9999999999)
        return random_part
    
    image_id = generate_unique_id()
    
    coco_data = {
        "info": {
            "description": "Orange Leaf Disease Classification Dataset",
            "version": "1.0",
            "year": 2025,
            "contributor": "Dataset maintainers",
            "source": "original",
            "license": {
                "name": "Creative Commons Attribution 4.0 International",
                "url": "https://creativecommons.org/licenses/by/4.0/"
            }
        },
        "images": [{
            "id": image_id,
            "width": width,
            "height": height,
            "file_name": filename,
            "size": 0,  # Will be updated if needed
            "format": "JPEG",
            "url": "",
            "hash": "",
            "status": "success"
        }],
        "annotations": [],
        "categories": [{
            "id": category_id,
            "name": category_name.replace('_', ' ').title(),
            "supercategory": "orange_leaf"
        }]
    }
    
    # Add annotations
    for i, ann in enumerate(annotations):
        coco_data["annotations"].append({
            "id": image_id + i,
            "image_id": image_id,
            "category_id": category_id,
            "segmentation": [],
            "area": ann['width'] * ann['height'],
            "bbox": [ann['x'], ann['y'], ann['width'], ann['height']],
            "iscrowd": 0
        })
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(coco_data, f, indent=2, ensure_ascii=False)

def create_dataset_splits(oranges_dir, all_images):
    """Create dataset split files"""
    random.seed(42)  # For reproducibility
    random.shuffle(all_images)
    
    total = len(all_images)
    train_size = int(total * 0.7)
    val_size = int(total * 0.15)
    # test_size = total - train_size - val_size
    
    train_images = all_images[:train_size]
    val_images = all_images[train_size:train_size + val_size]
    test_images = all_images[train_size + val_size:]
    
    # Create sets directory at category level
    sets_dir = oranges_dir / "sets"
    sets_dir.mkdir(exist_ok=True)
    
    # Write split files
    def write_split_file(filename, images):
        with open(sets_dir / filename, 'w', encoding='utf-8') as f:
            for subcategory, stem in images:
                f.write(f"{stem}\n")
    
    write_split_file("train.txt", train_images)
    write_split_file("val.txt", val_images)
    write_split_file("test.txt", test_images)
    write_split_file("all.txt", all_images)
    write_split_file("train_val.txt", train_images + val_images)
    
    print(f"\nDataset splits created:")
    print(f"  Train: {len(train_images)} images")
    print(f"  Val: {len(val_images)} images")
    print(f"  Test: {len(test_images)} images")
    print(f"  Total: {total} images")

if __name__ == "__main__":
    import sys
    
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    reorganize_dataset(root_dir)
    print("\nDataset reorganization completed!")





