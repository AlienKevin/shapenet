# Set up

## Build clip.cpp
```
cd clip.cpp

mkdir build

cd build

cmake -DCLIP_NATIVE=ON ..

make
```

# Download CLIP model
https://huggingface.co/mys/ggml_CLIP-ViT-B-32-laion2B-s34B-b79K/blob/main/CLIP-ViT-B-32-laion2B-s34B-b79K_ggml-model-q5_1.gguf

# Generate image embeddings
```
python embed_images.py ../snapshots/hat embeddings/snapshots/hat
```
