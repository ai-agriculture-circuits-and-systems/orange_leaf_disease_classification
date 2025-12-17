import os
import json
import random
import time
import re

def generate_unique_id():
    """Generate unique 7-digit random number + 3-digit timestamp"""
    random_part = random.randint(1000000, 9999999)
    timestamp_part = int(time.time() * 1000) % 1000
    return int(f"{random_part}{timestamp_part:03d}")

def extract_number_from_filename(filename):
    """Extract number from filename like 'Citrus Greening3.jpeg' -> 3"""
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else None

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

def parse_annotation_file(annotation_path):
    """Parse annotation file and return annotations"""
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
                        
                        # Convert normalized coordinates to pixel coordinates (assuming 512x512)
                        x = (x_center - width/2) * 512
                        y = (y_center - height/2) * 512
                        w = width * 512
                        h = height * 512
                        
                        annotations.append({
                            'category_id': category_id,
                            'bbox': [x, y, w, h],
                            'area': w * h
                        })
        except Exception as e:
            print(f"Error parsing annotation file {annotation_path}: {e}")
    return annotations

def get_category_mapping():
    """Get category mapping based on folder names"""
    return {
        'Citrus mealybugs': 1,
        'Spiny whitefly': 2,
        'Yellow dragon': 3,
        'Shot hole': 4,
        'Die back': 5,
        'Citrus canker': 6,
        'Yellow leaves': 7,
        'Powdery mildew': 8,
        'Citrus greening': 9,
        'Healthy leaf': 10,
        'Foliage damaged': 11
    }

def find_matching_annotation(image_filename, disease_name, annotation_dir):
    """Find matching annotation file based on naming pattern"""
    # Extract number from image filename
    number = extract_number_from_filename(image_filename)
    if number is None:
        return None
    
    # Normalize disease name for annotation format
    normalized_disease = normalize_disease_name(disease_name)
    
    # Try to find annotation file with matching number
    possible_names = [
        f"{normalized_disease} ({number}).txt",
        f"{normalized_disease} ({number}).jpg"
    ]
    
    for name in possible_names:
        annotation_path = os.path.join(annotation_dir, name)
        if os.path.exists(annotation_path):
            return annotation_path
    
    return None

def create_coco_annotation(image_path, category_name, annotation_data=None):
    """Create COCO format annotation for a single image"""
    # Generate unique IDs
    image_id = generate_unique_id()
    annotation_id = generate_unique_id()
    
    # Get category mapping
    category_mapping = get_category_mapping()
    category_id = category_mapping.get(category_name, 1)
    
    # Get image info
    image_name = os.path.basename(image_path)
    image_size = os.path.getsize(image_path)
    
    # Create COCO format
    coco_data = {
        "info": {
            "description": "data",
            "version": "1.0",
            "year": 2025,
            "contributor": "search engine",
            "source": "augmented",
            "license": {
                "name": "Creative Commons Attribution 4.0 International",
                "url": "https://creativecommons.org/licenses/by/4.0/"
            }
        },
        "images": [
            {
                "id": image_id,
                "width": 512,
                "height": 512,
                "file_name": image_name,
                "size": image_size,
                "format": "JPEG",
                "url": "",
                "hash": "",
                "status": "success"
            }
        ],
        "annotations": [],
        "categories": [
            {
                "id": category_id,
                "name": category_name,
                "supercategory": "Augmented Image"
            }
        ]
    }
    
    # Add annotations if available
    if annotation_data:
        for i, ann in enumerate(annotation_data):
            coco_data["annotations"].append({
                "id": annotation_id + i,
                "image_id": image_id,
                "category_id": ann["category_id"],
                "segmentation": [],
                "area": ann["area"],
                "bbox": ann["bbox"]
            })
    else:
        # Default annotation covering entire image
        coco_data["annotations"].append({
            "id": annotation_id,
            "image_id": image_id,
            "category_id": category_id,
            "segmentation": [],
            "area": 262144,
            "bbox": [0, 0, 512, 512]
        })
    
    return coco_data

def process_images_in_folder(folder_path, annotation_dir):
    """Process all images in a folder and generate COCO annotations"""
    category_mapping = get_category_mapping()
    
    for category_folder in os.listdir(folder_path):
        category_path = os.path.join(folder_path, category_folder)
        if os.path.isdir(category_path):
            category_name = category_folder
            
            for image_file in os.listdir(category_path):
                if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_path = os.path.join(category_path, image_file)
                    
                    # Find matching annotation using naming pattern
                    annotation_path = find_matching_annotation(image_file, category_name, annotation_dir)
                    annotation_data = None
                    
                    if annotation_path:
                        print(f"Found annotation for {image_file}: {annotation_path}")
                        annotation_data = parse_annotation_file(annotation_path)
                    else:
                        print(f"No annotation found for {image_file}")
                    
                    # Create COCO annotation
                    coco_data = create_coco_annotation(image_path, category_name, annotation_data)
                    
                    # Save JSON file in the same directory as the image
                    json_filename = os.path.splitext(image_file)[0] + '.json'
                    json_path = os.path.join(category_path, json_filename)
                    
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(coco_data, f, indent=2, ensure_ascii=False)
                    
                    print(f"Generated annotation for: {image_path}")

def main():
    """Main function to process both Original Image and Converted Image folders"""
    # Get script directory and project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)  # Go up one level from scripts/ to project root
    
    original_dir = os.path.join(base_dir, "data", "origin", "Original Image")
    converted_dir = os.path.join(base_dir, "data", "origin", "Converted Image")
    annotation_dir = os.path.join(base_dir, "data", "origin", "Annotation")
    
    print("Processing Original Image folder...")
    if os.path.exists(original_dir):
        process_images_in_folder(original_dir, annotation_dir)
    else:
        print(f"Original Image folder not found: {original_dir}")
    
    print("\nProcessing Converted Image folder...")
    if os.path.exists(converted_dir):
        process_images_in_folder(converted_dir, annotation_dir)
    else:
        print(f"Converted Image folder not found: {converted_dir}")
    
    print("\nAnnotation generation completed!")

if __name__ == "__main__":
    main() 