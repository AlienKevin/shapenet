How to use these scripts.

Note: You will need your own ChatgptAPI script. For the purposes of the this project I have provided my own. Don't abuse it please.
1. Create human made Description for an image file.

2. Use imagetotext.py to create a caption for the same image using hugging face model
    usage: python3 imagetotext.py <image_file>
    output: <image_filename>.huggingface.output

3. use GPTimagetotext.py to create a caption for the same iamge using chat gpt 4 API.
    usage: python3 GPTimagetotext.py <image_file>
    output: <image_filename>.GPTdesc.output

4. Use ROGUEcalc.py to find ROGUE scores for either generated description against the human made description.
    usage: python3 ROGUEcalc.py <generated_description_file> <human_description_file>
    output: <generated_description_file_name>.ROGUEcalc.output