"""Extract and print poly(A) tail sequences from BAM files.

The script looks for the `pt` tag (poly(A) tail length) that nanopore
basecallers such as Dorado emit. If the tag is missing, it falls back to
soft-clipped ends or the longest A/T run at the read termini.

Usage:
  python tests/print_polya_tails.py /home.galaxy4/sumin/project/ai-cosci/data/Q2 --max 50

Dependencies:
  - Requires `samtools` on $PATH for the fallback path (already available here).
  - If `pysam` is installed it will be used; otherwise the script streams
    alignments via `samtools view`.
"""
import argparse
import os
import subprocess
import sys
from typing import Iterable, Optional, Tuple

try:
    import pysam  # type: ignore
except ImportError:  # pragma: no cover
    pysam = None  # fallback to samtools view


def at_fraction(seq: str) -> float:
    """Fraction of As/Ts in a sequence chunk."""
    if not seq:
        return 0.0
    matches = sum(1 for base in seq if base in {"A", "a", "T", "t"})
    return matches / len(seq)


def pick_tail(seq: str, tail_len: int) -> str:
    """Select the best candidate tail from either end of the read."""
    if not seq or tail_len <= 0:
        return ""
    tail_len = min(tail_len, len(seq))
    left = seq[:tail_len]
    right = seq[-tail_len:]
    # Prefer the side that looks more A/T-rich; break ties by choosing the right end.
    return right if at_fraction(right) >= at_fraction(left) else left


def tail_from_cigar(seq: str, cigar: str, is_reverse: bool) -> str:
    """Get soft-clipped sequence (likely the tail) from CIGAR if present."""
    if not seq or cigar == "*":
        return ""
    # Parse minimal soft-clipping at either read end (e.g., 12S98M or 98M12S).
    soft_left = 0
    soft_right = 0
    num = ""
    ops = []
    for ch in cigar:
        if ch.isdigit():
            num += ch
        else:
            if not num:
                return ""  # malformed
            ops.append((ch, int(num)))
            num = ""
    if ops and ops[0][0] == "S":
        soft_left = ops[0][1]
    if ops and ops[-1][0] == "S":
        soft_right = ops[-1][1]

    left_seq = seq[:soft_left] if soft_left else ""
    right_seq = seq[-soft_right:] if soft_right else ""

    if is_reverse:
        candidates = [left_seq, right_seq]
    else:
        candidates = [right_seq, left_seq]

    return max(candidates, key=at_fraction, default="")


def extract_tail(seq: str, tail_len: Optional[int], cigar: str, is_reverse: bool) -> Tuple[str, str]:
    """Return tail sequence and the method used."""
    if tail_len:
        return pick_tail(seq, tail_len), "pt"

    cigar_tail = tail_from_cigar(seq, cigar, is_reverse)
    if cigar_tail:
        return cigar_tail, "cigar"

    # Fallback: take the most A/T-rich end chunk (up to 50 bases).
    fallback_len = min(50, len(seq))
    tail = pick_tail(seq, fallback_len)
    return tail, "heuristic"


def iter_records_with_pysam(bam_path: str) -> Iterable[Tuple[str, str, str, int]]:
    """Yield (read_name, tail, method, tail_length) using pysam."""
    assert pysam is not None
    with pysam.AlignmentFile(bam_path, "rb") as bam:
        for read in bam:
            seq = read.query_sequence or ""
            tail_len = read.get_tag("pt") if read.has_tag("pt") else None
            tail, method = extract_tail(seq, tail_len, read.cigarstring or "*", read.is_reverse)
            yield read.query_name, tail, method, len(tail)


def iter_records_with_samtools(bam_path: str) -> Iterable[Tuple[str, str, str, int]]:
    """Yield (read_name, tail, method, tail_length) using `samtools view`."""
    cmd = ["samtools", "view", bam_path]
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True) as proc:
        assert proc.stdout is not None
        try:
            for line in proc.stdout:
                fields = line.rstrip("\n").split("\t")
                if len(fields) < 11:
                    continue
                qname, flag_str, _rname, _pos, _mapq, cigar, _rnext, _pnext, _tlen, seq = fields[:10]
                if seq == "*":
                    seq = ""
                flag = int(flag_str)
                tags = fields[11:]
                tail_len = None
                for tag in tags:
                    if tag.startswith("pt:i:") or tag.startswith("PT:i:"):
                        try:
                            tail_len = int(tag.split(":")[2])
                            break
                        except (IndexError, ValueError):
                            continue
                tail, method = extract_tail(seq, tail_len, cigar, bool(flag & 16))
                yield qname, tail, method, len(tail)
        finally:
            if proc.poll() is None:
                proc.terminate()
            proc.wait()


def iter_bam_paths(path: str) -> Iterable[str]:
    """Expand a path that may be a BAM file or a directory of BAMs."""
    if os.path.isdir(path):
        for name in sorted(os.listdir(path)):
            if name.endswith(".bam"):
                yield os.path.join(path, name)
    else:
        yield path


def main() -> None:
    parser = argparse.ArgumentParser(description="Print poly(A) tail sequences from BAM files.")
    parser.add_argument("path", help="BAM file or directory containing BAMs.")
    parser.add_argument("--max", type=int, default=50, help="Maximum tails to print per BAM (default: 50).")
    args = parser.parse_args()

    for bam_path in iter_bam_paths(args.path):
        if not os.path.exists(bam_path):
            print(f"[warn] {bam_path} does not exist, skipping", file=sys.stderr)
            continue

        print(f"# {os.path.basename(bam_path)}")
        count = 0

        record_iter: Iterable[Tuple[str, str, str, int]]
        if pysam is not None:
            record_iter = iter_records_with_pysam(bam_path)
        else:
            record_iter = iter_records_with_samtools(bam_path)

        for read_name, tail_seq, method, tail_len in record_iter:
            if not tail_seq:
                continue
            print(f"{read_name}\tlen={tail_len}\tmethod={method}\t{tail_seq}")
            count += 1
            if count >= args.max:
                break

        if count == 0:
            print("  (no tails found)")


if __name__ == "__main__":
    main()
