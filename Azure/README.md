## Run the script 
Image Embedding: python3 mimage.py [replace snapshot folder name]

Text Embedding: python3 mtext.py [replace text description folder name]

embeddings.json: outputfile of each image embedding of each img file

eval.py: calculate a score out of 100 to evaluate how different cosine difference between different models

### Caution: The Azure charges starting $0.40 USD/1000 calls (Estimated). Avoid running the vectorizeImage unless necessary. The account only have $200 credit.