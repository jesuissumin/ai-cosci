p=$(cat problems/ex2.txt)
python -m src.cli \
  --question "$p" \
  --virtual-lab \
  --rounds 2 \
  --team-size 3 \
  --verbose \
  --output tests/q2.md \
  --combined \
  --input-dir data/Q2 