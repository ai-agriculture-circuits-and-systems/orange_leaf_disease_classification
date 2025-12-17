# Orange Leaf Disease Classification Dataset

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/your-repo/orange-leaf-disease-classification)

A comprehensive dataset of orange (citrus) leaf images for disease classification, collected and organized for computer vision and deep learning research in agricultural applications.

**Project page**: Dataset source information to be provided

## TL;DR

- **Task**: Classification, Object Detection
- **Modality**: RGB
- **Platform**: Ground/Field
- **Real/Synthetic**: Real
- **Images**: 4,749 orange leaf images across 11 categories (healthy_leaf, citrus_canker, citrus_greening, yellow_dragon, powdery_mildew, shot_hole, die_back, citrus_mealybugs, spiny_whitefly, yellow_leaves, foliage_damaged)
- **Resolution**: Variable (typically 480×640 pixels or larger)
- **Annotations**: CSV (per-image), COCO JSON (generated)
- **License**: CC BY 4.0
- **Citation**: see below

## Table of Contents

- [Download](#download)
- [Dataset Structure](#dataset-structure)
- [Sample Images](#sample-images)
- [Annotation Schema](#annotation-schema)
- [Stats and Splits](#stats-and-splits)
- [Quick Start](#quick-start)
- [Evaluation and Baselines](#evaluation-and-baselines)
- [Datasheet (Data Card)](#datasheet-data-card)
- [Known Issues and Caveats](#known-issues-and-caveats)
- [License](#license)
- [Citation](#citation)
- [Changelog](#changelog)
- [Contact](#contact)

## Download

**Original dataset**: Dataset source information to be provided

This repo hosts structure and conversion scripts only; place the downloaded folders under this directory.

**Local license file**: See `LICENSE` in the root directory.

## Dataset Structure

```
orange_leaf_disease_classification/
├── oranges/                                 # Main category directory
│   ├── healthy_leaf/                        # Healthy leaf subcategory
│   │   ├── csv/                             # CSV annotation files (per-image)
│   │   ├── json/                            # JSON annotation files (per-image)
│   │   ├── images/                          # Image files
│   │   └── sets/                            # Dataset split files (per-subcategory)
│   │       ├── train.txt                    # Training set image list
│   │       ├── val.txt                      # Validation set image list
│   │       ├── test.txt                     # Test set image list
│   │       ├── all.txt                      # All images list
│   │       └── train_val.txt                # Train+val images list
│   ├── citrus_canker/                       # Citrus canker subcategory
│   │   └── ...                             # Same structure as healthy_leaf
│   ├── citrus_greening/                     # Citrus greening subcategory
│   │   └── ...                             # Same structure as healthy_leaf
│   ├── yellow_dragon/                       # Yellow dragon subcategory
│   │   └── ...                             # Same structure as healthy_leaf
│   ├── powdery_mildew/                      # Powdery mildew subcategory
│   │   └── ...                             # Same structure as healthy_leaf
│   ├── shot_hole/                           # Shot hole subcategory
│   │   └── ...                             # Same structure as healthy_leaf
│   ├── die_back/                            # Die back subcategory
│   │   └── ...                             # Same structure as healthy_leaf
│   ├── citrus_mealybugs/                     # Citrus mealybugs subcategory
│   │   └── ...                             # Same structure as healthy_leaf
│   ├── spiny_whitefly/                      # Spiny whitefly subcategory
│   │   └── ...                             # Same structure as healthy_leaf
│   ├── yellow_leaves/                       # Yellow leaves subcategory
│   │   └── ...                             # Same structure as healthy_leaf
│   ├── foliage_damaged/                     # Foliage damaged subcategory
│   │   └── ...                             # Same structure as healthy_leaf
│   └── labelmap.json                        # Label mapping file
│
├── annotations/                             # COCO format JSON files (generated)
│   ├── healthy_leaf_instances_train.json
│   ├── healthy_leaf_instances_val.json
│   ├── healthy_leaf_instances_test.json
│   ├── citrus_canker_instances_*.json
│   ├── citrus_greening_instances_*.json
│   ├── yellow_dragon_instances_*.json
│   ├── powdery_mildew_instances_*.json
│   ├── shot_hole_instances_*.json
│   ├── die_back_instances_*.json
│   ├── citrus_mealybugs_instances_*.json
│   ├── spiny_whitefly_instances_*.json
│   ├── yellow_leaves_instances_*.json
│   ├── foliage_damaged_instances_*.json
│   └── combined_instances_*.json            # Combined multi-category files
│
├── scripts/                                 # Utility scripts
│   ├── reorganize_data.py                   # Reorganize dataset to standard structure
│   ├── convert_to_coco.py                   # Convert CSV to COCO format
│   └── generate_coco_annotations.py         # Original COCO annotation generator
│
├── data/                                    # Data directory
│   └── origin/                              # Original data (preserved)
│       ├── Original Image/                  # Original high-resolution images
│       │   └── ...
│       └── Annotation/                     # Original YOLO format annotations
│           └── ...
│
├── LICENSE                                  # License file
├── README.md                                # This file
└── requirements.txt                         # Python dependencies
```

**Splits**: Splits provided via `oranges/{subcategory}/sets/*.txt`. List image basenames (no extension). If missing, all images are used.

## Sample Images

<table>
  <tr>
    <th>Category</th>
    <th>Sample</th>
  </tr>
  <tr>
    <td><strong>Healthy Leaf</strong></td>
    <td>
      <img src="oranges/healthy_leaf/images/Healthy Leaf100.jpeg" alt="Healthy orange leaf" width="260"/>
      <div align="center"><code>oranges/healthy_leaf/images/Healthy Leaf100.jpeg</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Citrus Canker</strong></td>
    <td>
      <img src="oranges/citrus_canker/images/Citrus Canker1.jpeg" alt="Citrus canker on orange leaf" width="260"/>
      <div align="center"><code>oranges/citrus_canker/images/Citrus Canker1.jpeg</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Citrus Greening</strong></td>
    <td>
      <img src="oranges/citrus_greening/images/Citrus Greening1.jpeg" alt="Citrus greening on orange leaf" width="260"/>
      <div align="center"><code>oranges/citrus_greening/images/Citrus Greening1.jpeg</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Yellow Dragon</strong></td>
    <td>
      <img src="oranges/yellow_dragon/images/Yellow Dragon1.jpeg" alt="Yellow dragon disease on orange leaf" width="260"/>
      <div align="center"><code>oranges/yellow_dragon/images/Yellow Dragon1.jpeg</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Powdery Mildew</strong></td>
    <td>
      <img src="oranges/powdery_mildew/images/Powdery Mildew1.jpeg" alt="Powdery mildew on orange leaf" width="260"/>
      <div align="center"><code>oranges/powdery_mildew/images/Powdery Mildew1.jpeg</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Shot Hole</strong></td>
    <td>
      <img src="oranges/shot_hole/images/Shot Hole1.jpeg" alt="Shot hole disease on orange leaf" width="260"/>
      <div align="center"><code>oranges/shot_hole/images/Shot Hole1.jpeg</code></div>
    </td>
  </tr>
</table>

## Annotation Schema

### CSV Format

Each image has a corresponding CSV annotation file in `oranges/{subcategory}/csv/{image_name}.csv`:

```csv
#item,x,y,width,height,label
0,0.00,0.00,480.00,640.00,1
```

- **Coordinates**: `x, y` - top-left corner of bounding box (pixels)
- **Dimensions**: `width, height` - bounding box dimensions (pixels)
- **Label**: Category ID (1=healthy_leaf, 2=citrus_canker, 3=citrus_greening, 4=yellow_dragon, 5=powdery_mildew, 6=shot_hole, 7=die_back, 8=citrus_mealybugs, 9=spiny_whitefly, 10=yellow_leaves, 11=foliage_damaged)

For classification tasks, the bounding box typically covers the entire image `[0, 0, image_width, image_height]`.

### COCO Format

COCO format JSON files are generated in the `annotations/` directory. Example structure:

```json
{
  "info": {
    "year": 2025,
    "version": "1.0",
    "description": "Orange Leaf Disease Classification healthy_leaf train split",
    "url": ""
  },
  "images": [
    {
      "id": 1234567890,
      "file_name": "oranges/healthy_leaf/images/Healthy Leaf100.jpeg",
      "width": 480,
      "height": 640
    }
  ],
  "annotations": [
    {
      "id": 1,
      "image_id": 1234567890,
      "category_id": 1,
      "bbox": [0, 0, 480, 640],
      "area": 307200,
      "iscrowd": 0
    }
  ],
  "categories": [
    {"id": 0, "name": "background", "supercategory": "background"},
    {"id": 1, "name": "healthy_leaf", "supercategory": "orange_leaf"},
    {"id": 2, "name": "citrus_canker", "supercategory": "orange_leaf"},
    {"id": 3, "name": "citrus_greening", "supercategory": "orange_leaf"},
    {"id": 4, "name": "yellow_dragon", "supercategory": "orange_leaf"},
    {"id": 5, "name": "powdery_mildew", "supercategory": "orange_leaf"},
    {"id": 6, "name": "shot_hole", "supercategory": "orange_leaf"},
    {"id": 7, "name": "die_back", "supercategory": "orange_leaf"},
    {"id": 8, "name": "citrus_mealybugs", "supercategory": "orange_leaf"},
    {"id": 9, "name": "spiny_whitefly", "supercategory": "orange_leaf"},
    {"id": 10, "name": "yellow_leaves", "supercategory": "orange_leaf"},
    {"id": 11, "name": "foliage_damaged", "supercategory": "orange_leaf"}
  ]
}
```

### Label Maps

Label mapping is defined in `oranges/labelmap.json`:

```json
[
  {"object_id": 0, "label_id": 0, "keyboard_shortcut": "0", "object_name": "background"},
  {"object_id": 1, "label_id": 1, "keyboard_shortcut": "1", "object_name": "healthy_leaf"},
  {"object_id": 2, "label_id": 2, "keyboard_shortcut": "2", "object_name": "citrus_canker"},
  {"object_id": 3, "label_id": 3, "keyboard_shortcut": "3", "object_name": "citrus_greening"},
  {"object_id": 4, "label_id": 4, "keyboard_shortcut": "4", "object_name": "yellow_dragon"},
  {"object_id": 5, "label_id": 5, "keyboard_shortcut": "5", "object_name": "powdery_mildew"},
  {"object_id": 6, "label_id": 6, "keyboard_shortcut": "6", "object_name": "shot_hole"},
  {"object_id": 7, "label_id": 7, "keyboard_shortcut": "7", "object_name": "die_back"},
  {"object_id": 8, "label_id": 8, "keyboard_shortcut": "8", "object_name": "citrus_mealybugs"},
  {"object_id": 9, "label_id": 9, "keyboard_shortcut": "9", "object_name": "spiny_whitefly"},
  {"object_id": 10, "label_id": 10, "keyboard_shortcut": "a", "object_name": "yellow_leaves"},
  {"object_id": 11, "label_id": 11, "keyboard_shortcut": "b", "object_name": "foliage_damaged"}
]
```

## Stats and Splits

### Image Statistics

| Category | Total |
|----------|-------|
| Healthy Leaf | 594 |
| Citrus Canker | 588 |
| Citrus Greening | 254 |
| Yellow Dragon | 407 |
| Powdery Mildew | 598 |
| Shot Hole | 560 |
| Die Back | 434 |
| Citrus Mealybugs | 603 |
| Spiny Whitefly | 677 |
| Yellow Leaves | 34 |
| Foliage Damaged | 0 |
| **Total** | **4,749** |

### Split Distribution

- **Training set**: 70% (3,324 images)
- **Validation set**: 15% (712 images)
- **Test set**: 15% (713 images)

Splits provided via `oranges/{subcategory}/sets/*.txt`. You may define your own splits by editing those files.

## Quick Start

### Load COCO Format Annotations

```python
from pycocotools.coco import COCO
import matplotlib.pyplot as plt

# Load COCO annotation file
coco = COCO('annotations/combined_instances_train.json')

# Get all image IDs
img_ids = coco.getImgIds()
print(f"Total images: {len(img_ids)}")

# Get all category IDs
cat_ids = coco.getCatIds()
print(f"Categories: {[coco.loadCats(cat_id)[0]['name'] for cat_id in cat_ids]}")

# Load a specific image and its annotations
img_id = img_ids[0]
img_info = coco.loadImgs(img_id)[0]
ann_ids = coco.getAnnIds(imgIds=img_id)
anns = coco.loadAnns(ann_ids)

print(f"Image: {img_info['file_name']}")
print(f"Annotations: {len(anns)}")
```

### Convert CSV to COCO Format

```bash
# Convert all categories to COCO format
python scripts/convert_to_coco.py --root . --out annotations --combined

# Convert specific categories
python scripts/convert_to_coco.py --root . --out annotations \
    --categories healthy_leaf citrus_canker --splits train val test

# Generate combined files
python scripts/convert_to_coco.py --root . --out annotations --combined
```

### Dependencies

**Required**:
- Python 3.6+
- Pillow>=9.5

**Optional** (for COCO API):
- pycocotools>=2.0.7

Install dependencies:
```bash
pip install -r requirements.txt
```

## Evaluation and Baselines

### Evaluation Metrics

For classification tasks, common metrics include:
- **Accuracy**: Overall classification accuracy
- **Precision, Recall, F1-Score**: Per-class and macro-averaged metrics
- **Confusion Matrix**: Per-class classification performance

For object detection tasks:
- **mAP@[.50:.95]**: Mean Average Precision at IoU thresholds from 0.5 to 0.95
- **mAP@0.5**: Mean Average Precision at IoU threshold 0.5

### Baseline Results

*Baseline results will be added as they become available.*

## Datasheet (Data Card)

### Motivation

This dataset was created to support research in automated plant disease detection and classification, specifically for orange (citrus) leaves. The dataset enables the development of computer vision models for early disease detection in agricultural applications.

### Composition

The dataset contains:
- **4,749 images** of orange (citrus) leaves
- **11 disease/health categories**: healthy_leaf, citrus_canker, citrus_greening, yellow_dragon, powdery_mildew, shot_hole, die_back, citrus_mealybugs, spiny_whitefly, yellow_leaves, foliage_damaged
- **Per-image annotations** in CSV and COCO JSON formats
- **Full-image bounding boxes** for classification tasks

### Collection Process

- Images were collected from various sources and processed for orange leaf disease research
- Images include both original and converted versions
- Annotations were created using custom scripts converting from YOLO format to CSV and COCO formats

### Preprocessing

- Images are organized by disease category
- Standardized directory structure following the dataset organization guidelines
- CSV and COCO JSON annotations generated for each image
- Dataset splits created with 70/15/15 ratio (train/val/test)

### Distribution

The dataset is distributed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

### Maintenance

The dataset is maintained by the community. Issues and contributions are welcome.

## Known Issues and Caveats

1. **Image Resolution**: Images have variable resolutions, typically 480×640 pixels or larger. Models should handle variable input sizes or resize images appropriately.

2. **Annotation Format**: For classification tasks, annotations use full-image bounding boxes `[0, 0, width, height]`. The category ID in the annotation indicates the image class.

3. **File Naming**: Original image files use various naming conventions. The standardized structure preserves meaningful filenames while ensuring consistency.

4. **Data Source**: The dataset includes original data in `data/origin/` directory. The standardized structure uses converted images (now in `oranges/{subcategory}/images/`). Original data is preserved in `data/origin/` for reference.

5. **Coordinate System**: Bounding box coordinates use the standard image coordinate system with origin (0,0) at the top-left corner.

6. **Class Imbalance**: Some categories have significantly fewer images than others (e.g., yellow_leaves has only 34 images, foliage_damaged has 0 images). Users should be aware of this imbalance when training models.

## License

This dataset is licensed under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**.

See the `LICENSE` file in the root directory for the full license text.

**Summary**: You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made.

Check the original dataset terms and cite appropriately.

## Citation

If you use this dataset in your research, please cite:

```bibtex
@dataset{orange_leaf_disease_classification_2025,
  title={Orange Leaf Disease Classification Dataset},
  author={Dataset Contributors},
  year={2025},
  url={},
  license={CC BY 4.0}
}
```

## Changelog

- **V1.0.0** (2025-12): Initial standardized structure and COCO conversion utility
  - Reorganized dataset to standard structure following dataset organization guidelines
  - Created CSV and COCO JSON annotations
  - Generated dataset splits (train/val/test)
  - Added conversion scripts and documentation

## Contact

**Maintainers**: Dataset maintainers

**Original Authors**: Dataset contributors

**Source**: Dataset source information to be provided

For questions, issues, or contributions, please open an issue or submit a pull request.
