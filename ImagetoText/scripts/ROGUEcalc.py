from rouge_score import rouge_scorer
import sys
import os

def read_file(file_path):
    """Reads the content of a file."""
    with open(file_path, 'r') as file:
        return file.read().strip()

def write_output(output_path, generated_description, human_description, scores):
    """Writes the input texts and ROUGE scores to an output file."""
    with open(output_path, 'w') as file:
        file.write("Generated Description:\n")
        file.write(generated_description + "\n\n")
        file.write("Human Description:\n")
        file.write(human_description + "\n\n")
        file.write("ROUGE Scores:\n")
        for key, value in scores.items():
            file.write(f"{key}: {value}\n")

def compute_rouge_scores(generated_description, human_description):
    """Computes ROUGE scores for the generated and human descriptions."""
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(generated_description, human_description)
    return {key: value.fmeasure for key, value in scores.items()}

def main(generated_file_path, human_file_path):
    # Read the content of the input files
    generated_description = read_file(generated_file_path)
    human_description = read_file(human_file_path)

    # Compute the ROUGE scores
    scores = compute_rouge_scores(generated_description, human_description)

    # Construct the output file name
    base_name = os.path.splitext(generated_file_path)[0]
    output_file_path = f"{base_name}.ROGUEcalc.output"

    # Write the results to the output file
    write_output(output_file_path, generated_description, human_description, scores)

    # Print a message indicating success
    print(f"Results written to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <generated_description_file> <human_description_file>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
