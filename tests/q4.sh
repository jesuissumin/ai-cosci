p=$(cat problems/ex4.txt)
python -m src.cli \
  --question "$p" \
  --virtual-lab \
  --rounds 2 \
  --team-size 3 \
  --verbose \
  --output tests/q4.md \
  --combined 