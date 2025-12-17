
import pysam
import os
import argparse

def find_mixed_tails_with_pt_tag(bam_file, limit=50):
    """
    Finds and prints mixed tails and their lengths from a BAM file using the 'pt' tag.
    The 'pt' tag is assumed to contain the length of the tail.
    """
    print(f"Processing file: {bam_file} (using pt tag for mixed tails)")
    count = 0
    with pysam.AlignmentFile(bam_file, "rb") as bam:
        for read in bam:
            if count >= limit:
                break
            if read.has_tag('pt'):
                tail_length = read.get_tag('pt')
                if tail_length > 0 and read.query_sequence:
                    sequence = read.query_sequence
                    if len(sequence) >= tail_length:
                        tail = sequence[-tail_length:]
                        print(f"Sequence: {tail}, Length: {len(tail)}")
                        count += 1

def find_mixed_tails_with_cigar(bam_file, limit=50):
    """
    Finds and prints mixed tails and their lengths from a BAM file using CIGAR string soft clipping.
    """
    print(f"Processing file: {bam_file} (using CIGAR soft clip for mixed tails)")
    count = 0
    with pysam.AlignmentFile(bam_file, "rb") as bam:
        for read in bam:
            if count >= limit:
                break
            if read.cigartuples and read.query_sequence:
                # Check for soft clipping at the end of the read
                if read.cigartuples[-1][0] == 4:  # BAM_CSOFT_CLIP
                    clip_length = read.cigartuples[-1][1]
                    sequence = read.query_sequence
                    soft_clipped_seq = sequence[-clip_length:]
                    print(f"Sequence: {soft_clipped_seq}, Length: {len(soft_clipped_seq)}")
                    count += 1

def main():
    parser = argparse.ArgumentParser(description="Find mixed tails in BAM files using two methods and print sequence and length.")
    parser.add_argument("bam_directory", help="Directory containing BAM files.")
    args = parser.parse_args()

    for filename in os.listdir(args.bam_directory):
        if filename.endswith(".bam"):
            bam_file_path = os.path.join(args.bam_directory, filename)
            find_mixed_tails_with_pt_tag(bam_file_path)
            print("-" * 20)
            find_mixed_tails_with_cigar(bam_file_path)
            print("=" * 20)

if __name__ == "__main__":
    main()
