# Multimodal 3D Shape Retrieval with Sketch and Text

This is the repository for all the code and data used for the paper titled "Multimodal 3D Shape Retrieval with Sketch and Text" by Xiang Li, Yuyao Huang, Ethan Chau, Zaid Shahid, and Ashwin Kumar.

# Our Dataset
## 3D Shapes
We annotated 113 3D objects in the camera category of the ShapeNetCore dataset. You can find the original OBJ shapes from that dataset under `objs/02942699/`, where `02942699` is the original id for the camera category.

## Snapshots
For each camera shape, we generate 3 snapshots from angles of 0, 30, and 75 degrees. You can find these snapshots under `snapshots/camera/`. The file name follows the format of `{shape_id}_{angle_id}.png`, where the angle_id is 1 for 0 degrees, 2 for 30 degrees, and 3 for 75 degrees angle.

## Sketches
For each camera shape, we generate 1 sketch at a random angle among 0, 30, and 75 using CLIPasso. You can find the generated SVG sketches under `sketches/`. The file name follows the format of `{shape_id}_{angle_id}.svg`. For use to compute image embeddings, the SVGs have been converted into PNGs under the `sketches-png/` folder.

You can find the hand-drawn sketches under `sketches-manual-png/`. The manual sketches are drawn from a natural angle as see fit by the author, so it does not adhere to one of the 0, 30, and 75 angles used for generated sketches. The file name follows the format of `{shape_id}_sketch.png`.

## Captions
We generate two types of captions for the snapshots. One is the system description of each snapshot used internally for retrieval. The other is a simulated user query looking for a shape. We also manually write user queries for a shape. To simulate user queries in a different style from system descriptions, we use two distinct LLMs to generate each caption. We use Gemini 1.0 Pro Vision for the system descriptions and GPT-4 Vision for the simulated user queries.

The system descriptions and simulated user queries can be found under `ImagetoText/ImagetoTextOutput/` where the file names follow the format of `{shape_id}_{angle_id}_{caption_llm}`. You can find the manually-written user queries under `snapshots/camera_queries/` where the file names follow the format of `{shape_id}.txt`. The `ImagetoText/` folder also contains scripts used to generate those embeddings. See the `ImagetoText/README.txt` for details.

To experiment if we can convert all modalities to text and compute similarities using text embeddings alone, we also generate captions for sketches. You can find the captions for the CLIPasso-generated sketches under `ImagetoText/SketchesImagetoTextOutput/` and the hand-drawn sketches under `ImagetoText/ManualSketchesImagetoTextOutput`. These two folders have identical folder structure:
- `camera_embeddings`: embeddings for snapshots
- `camera_queries_embeddings`: embeddings for manually-written user queries
- `ImagetoTextOutput_embeddings`: embeddings for system descriptions
- `ManualSketchesImagetoTextOutput_embeddings`: embeddings for captions of hand-drawn sketches
- `sketches-manual-png_embeddings`: embeddings for hand-drawn sketches
- `sketches-png_embeddings`: embeddings for CLIPasso-generated sketches
- `SketchesImagetoTextOutput_embeddings`: embeddings for captions of CLIPasso-generated sketches

## Text and Image Embeddings
We generate text and image embeddings using two off-the-shelf multimodal embedding models. You can find the Microsoft Azure embeddings under `azure/` and the Google Vertex embeddings under `vertex/`. The `azure/` and `vertex/` folders also contain scripts used to generate those embeddings. See the `README.md` in each folder for details.

# Environment Setup
```
conda create -n multimodal3d -c conda-forge python=3.12 tqdm scipy numpy matplotlib replicate pillow requests rouge-score click google-cloud-aiplatform
conda activate multimodal3d
python -m pip install -U google-generativeai azure-cognitiveservices-vision-computervision
```
If you choose to set up your own virtual environment, remember to use Python version 3.12.

# Run main experiment
You can generate the main experiment plot by running:
```
python search.py --approach all --k 1 --embedding_model azure
```
You should see a plot named `percent_top_1_hits_azure.png` as a result.

In the paper, we vary k to be `1`, `5`, and `10` to analyze precision at different values of top k.
We also experiment with two embedding_models: `azure` and `vertex`.

You can compare the percent hits performance of text-only, sketch-only, and weighted-sum (image-weight=0.6) by running:
```
python calculate_percent_increase.py
```
Expected output is:
```
K = 1
Percent increase from text-only to image-weight=0.6: 48%
Percent increase from sketch-only to image-weight=0.6: 34%
K = 5
Percent increase from text-only to image-weight=0.6: 39%
Percent increase from sketch-only to image-weight=0.6: 13%
K = 10
Percent increase from text-only to image-weight=0.6: 20%
Percent increase from sketch-only to image-weight=0.6: 10%
```
Note that the experiments results are hard coded into this script. To use the values you got from running the main experiment, you can
overwrite the `k1_human_weighted_sum_top_k_hits` and `k1_machine_weighted_sum_top_k_hits` etc in `calculate_percent_increase.py`.

# Generate snapshots (macOS only)
We had trouble finding reliable OBJ renderers in Python, so we resort to using macOS's SceneKit to render OBJ files into snapshot images in Swift.

1. Open `objViewer/objViewer.xcodeproj` in Xcode

2. Hit the Run button on the top left to generate snapshots

3. Copy the generated folder into `objs/02942699`

# Set up CLIPasso

1. Install replicate
```
python -m pip install replicate
```

2. Export api token
```
export REPLICATE_API_TOKEN=r8_HvGxxx
```

3. Run cilpasso to generate 113 SVG sketches
```
python clipasso.py
```

4. Convert SVG sketches to PNG
```
python convert_sketches_to_png.py
```
