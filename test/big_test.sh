set -x
if [ ! -f "actual/create_csv_file.out" ]; then
  python ../code/main.py scripts/create_csv_file.txt > actual/create_csv_file.out
  diff expected/create_csv_file.out actual/create_csv_file.out
fi
