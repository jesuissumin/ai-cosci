
import pysam
import os
import argparse

def is_polya_tail(sequence, polya_ratio=0.8):
    """
    Checks if a sequence is a poly(A) tail.
    A sequence is considered a poly(A) tail if the ratio of 'A's is above a certain threshold.
    """
    if not sequence:
        return False
    return sequence.count('A') / len(sequence) >= polya_ratio

def print_polya_tails(bam_file):
    """
    Finds and prints poly(A) tails from a BAM file using CIGAR string soft clipping.
    """
    print(f"Processing file: {bam_file}")
    with pysam.AlignmentFile(bam_file, "rb") as bam:
        for read in bam:
            if read.cigartuples and read.query_sequence:
                # Check for soft clipping at the end of the read
                if read.cigartuples[-1][0] == 4:  # BAM_CSOFT_CLIP
                    clip_length = read.cigartuples[-1][1]
                    sequence = read.query_sequence
                    soft_clipped_seq = sequence[-clip_length:]
                    if is_polya_tail(soft_clipped_seq):
                        print(f"Poly(A) tail found: {soft_clipped_seq}")

def main():
    parser = argparse.ArgumentParser(description="Print poly(A) tail sequences from BAM files.")
    parser.add_argument("bam_directory", help="Directory containing BAM files.")
    args = parser.parse_args()

    for filename in os.listdir(args.bam_directory):
        if filename.endswith(".bam"):
            bam_file_path = os.path.join(args.bam_directory, filename)
            print_polya_tails(bam_file_path)
            print("-" * 20)

if __name__ == "__main__":
    main()
