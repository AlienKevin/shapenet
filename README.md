# Main Experiment Setup
```
conda create -n multimodal3d -c conda-forge tqdm scipy numpy matplotlib
conda activate multimodal3d
```

# Run main experiment
You can generate the main experiment plot by running:
```
python search.py --approach all --k 1 --embedding_model vertex
```
In the paper, we vary k to be 1, 5, and 10 to analyze precision at different values of top k.
We also experiment with embedding_model=vertex and azure.

# Set up Clipasso

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
