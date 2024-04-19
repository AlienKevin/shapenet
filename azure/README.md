## How to Run the script 

Dependency: 
pip install azure-cognitiveservices-vision-computervision
pip install numpy
pip install requests

Image Embedding: python3 mimage.py [replace snapshot folder name]
Text Embedding: python3 mtext.py [replace text description folder name]\

The API keys in the script is listed xxx, put in your own account endpoint to run.

For image embedding, each embedding would be saved to an individual file
For text embedding, inside each source folder, a new folder called "textemb" would be created containing all the embeddings.
