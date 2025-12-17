p=$(cat problems/ex3.txt)
python -m src.cli \
  --question "$p" \
  --virtual-lab \
  --rounds 2 \
  --team-size 3 \
  --verbose \
  --output tests/q3.md \
  --combined 