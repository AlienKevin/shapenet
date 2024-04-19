How to use these scripts.

Note: You will need your own ChatgptAPI script. For the purposes of the this project I have provided my own. Don't abuse it please.
1. Create human made Description for an image file.

2. Use Geminiimagetotext.py to create a caption for the same image using Gemini 1.0 Pro Vision.
    usage: python3 Geminiimagetotext.py <image_file>
        ex: python3 Geminiimagetotext.py imageofchair.jpg
    output: <image_filename>.Gemini.npy

3. use GPTimagetotext.py to create a caption for the same iamge using GPT-4 Vision API.
    usage: python3 GPTimagetotext.py <image_file>
        ex: python3 GPTimagetotext.py imageofchair.jpg
    output: <image_filename>.GPTdesc.npy

4. Use ROGUEcalc.py to find ROGUE scores for either generated description against the human made description.
    usage: python3 ROGUEcalc.py <generated_description_file> <human_description_file>
    output: <generated_description_file_name>.ROGUEcalc.output

Also there is a driver script that will take in a folder and go through each image in the folder and get the captions for each image.
In order to use driver.py this is what is needed
- A folder containing the images
- Both the Gemini and GPT image to text scripts
- Make sure to have the api keys within the scripts 

usage: python3 driver.py <image_folder>
    ex: python3 driver.py ../sketches-png
output: folder containing two files for each image. One GPT file and one for Gemini
        file name for output looks like filename_<GPT/Gemini>.npy
