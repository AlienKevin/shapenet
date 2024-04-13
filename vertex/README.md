# Description

Generates Google multimodal embeddings of files within a directory. Creates an output directory for each input directory with '_embedding' appended to the directory name inside the vertex directory.

# Usage

Modify PROJECT_ID and REGION to match google cloud project id and region.

google_embeddings.py
- '-i, ---img_dir': The path to a directory containing image files ( accepts multiple)
- '-t, ---txt_dir': The path to a directory containing text files (accepts multiple)

Example from shapenet root: python3 vertex/google_embeddings.py -i snapshots/camera -t ImagetoText/ImagetoTextOutput 

**Warning:** Repeated directory names will overwrite each other so make sure input directory names are unique.