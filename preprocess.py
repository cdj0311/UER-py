import argparse
import torch
from uer.utils.data import *
from uer.utils.tokenizer import *


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Path options.
    parser.add_argument("--corpus_path", type=str, required=True,
                        help="Path of the corpus for pretraining.")
    parser.add_argument("--vocab_path", default=None, type=str,
                        help="Path of the vocabulary file.")
    parser.add_argument("--spm_model_path", default=None, type=str,
                        help="Path of the sentence piece model.")
    parser.add_argument("--dataset_path", type=str, default="dataset.pt",
                        help="Path of the preprocessed dataset.")

    # Preprocess options.
    parser.add_argument("--tokenizer", choices=["bert", "char", "space"], default="bert",
                        help="Specify the tokenizer." 
                             "Original Google BERT uses bert tokenizer on Chinese corpus."
                             "Char tokenizer segments sentences into characters."
                             "Space tokenizer segments sentences into words according to space."
                             )
    parser.add_argument("--processes_num", type=int, default=1,
                        help="Split the whole dataset into `processes_num` parts, "
                             "and each part is fed to a single process in training step.")
    parser.add_argument("--target", choices=["bert", "lm", "cls", "mlm", "bilm", "albert"], default="bert",
                        help="The training target of the pretraining model.")
    parser.add_argument("--docs_buffer_size", type=int, default=100000,
                        help="The buffer size of documents in memory, specific to targets that require negative sampling.")
    parser.add_argument("--seq_length", type=int, default=128, help="Sequence length of instances.")
    parser.add_argument("--dup_factor", type=int, default=5,
                        help="Duplicate instances multiple times.")
    parser.add_argument("--short_seq_prob", type=float, default=0.1,
                        help="Probability of truncating sequence."
                             "The larger value, the higher probability of using short (truncated) sequence.")
    parser.add_argument("--full_sentences", action="store_true", help="Full sentences.")
    parser.add_argument("--seed", type=int, default=7, help="Random seed.")

    # Masking options.
    parser.add_argument("--dynamic_masking", action="store_true", help="Dynamic masking.")
    parser.add_argument("--span_masking", action="store_true", help="Span masking.")
    parser.add_argument("--span_geo_prob", type=float, default=0.2,
                        help="Hyperparameter of geometric distribution for span masking.")
    parser.add_argument("--span_max_length", type=int, default=10,
                        help="Max length for span masking.")

    args = parser.parse_args()

    # Dynamic masking.
    if args.dynamic_masking:
        args.dup_factor = 1

    # Build tokenizer.
    tokenizer = globals()[args.tokenizer.capitalize() + "Tokenizer"](args)

    # Build and save dataset.
    dataset = globals()[args.target.capitalize() + "Dataset"](args, tokenizer.vocab, tokenizer)
    dataset.build_and_save(args.processes_num)


if __name__ == "__main__":
    main()
