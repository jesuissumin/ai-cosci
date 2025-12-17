p=$(cat problems/ex1.txt)
python -m src.cli \
  --question "$p" \
  --virtual-lab \
  --rounds 2 \
  --team-size 3 \
  --verbose \
  --output tests/q1.md \
  --combined \
  --input-dir data/Q1 