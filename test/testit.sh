set -x
if [ ! -f "actual/bar_graph_1.out" ]; then
  python ../code/main.py scripts/bar_graph_1.txt > actual/bar_graph_1.out
  diff expected/bar_graph_1.out actual/bar_graph_1.out
  mv bar_graph_1.csv actual
  diff expected/bar_graph_1.csv actual
  mv bar_graph_1.png actual
  diff -b expected/bar_graph_1.png actual
fi
if [ ! -f "actual/create_column.out" ]; then
  python ../code/main.py scripts/create_column.txt > actual/create_column.out
  diff expected/create_column.out actual/create_column.out
fi

# if [ ! -f "actual/noinput.out" ]; then
#   python ../pd.py scripts/noinput.txt > actual/noinput.out
#   diff expected/noinput.out actual/noinput.out
# fi
# if [ ! -f "actual/badsyntax.out" ]; then
#   python ../pd.py scripts/badsyntax.txt > actual/badsyntax.out
#   diff expected/badsyntax.out actual/badsyntax.out
# fi
# if [ ! -f "actual/load_data_1.out" ]; then
#   python ../pd.py scripts/load_data_1.txt > actual/load_data_1.out
#   diff expected/load_data_1.out actual/load_data_1.out
# fi
# if [ ! -f "actual/drop_columns.out" ]; then
#   python ../pd.py scripts/drop_columns.txt > actual/drop_columns.out
#   diff expected/drop_columns.out actual/drop_columns.out
# fi
# if [ ! -f "actual/save_data_1.out" ]; then
#   python ../pd.py scripts/save_data_1.txt > actual/save_data_1.out
#   diff expected/save_data_1.out actual/save_data_1.out
#   mv sample20.csv actual
#   diff expected/sample20.csv actual
# fi
# if [ ! -f "actual/all_areas.csv" ]; then
#   python ../pd.py scripts/create_csv_file.txt > actual/create_csv_file.out
#   diff expected/create_csv_file.out actual/create_csv_file.out
#   mv all_areas.csv actual
#   diff expected/all_areas.csv actual
# fi
# if [ ! -f "actual/draw_graph_1.out" ]; then
#   python ../pd.py scripts/draw_graph_1.txt > actual/draw_graph_1.out
#   diff expected/draw_graph_1.out actual/draw_graph_1.out
#   mv *.png actual
#   mv *.csv actual
#   diff -b expected/77th_Street.png actual
#   diff -b expected/Central.png actual
#   diff -b expected/Central.png actual
#   diff -b expected/Devonshire.png actual
#   diff -b expected/Foothill.png actual
#   diff -b expected/Harbor.png actual
#   diff -b expected/Hollenbeck.png actual
#   diff -b expected/Hollywood.png actual
#   diff -b expected/Mission.png actual
#   diff -b expected/N_Hollywood.png actual
#   diff -b expected/Newton.png actual
#   diff -b expected/Northeast.png actual
#   diff -b expected/Olympic.png actual
#   diff -b expected/Pacific.png actual
#   diff -b expected/Rampart.png actual
#   diff -b expected/Southeast.png actual
#   diff -b expected/Southwest.png actual
#   diff -b expected/Topanga.png actual
#   diff -b expected/Van_Nuys.png actual
#   diff -b expected/West_LA.png actual
#   diff -b expected/West_Valley.png actual
#   diff -b expected/Wilshire.png actual
#   diff expected/all_areas.Area_Name.77th_Street.csv actual
#   diff expected/all_areas.Area_Name.Central.csv actual
#   diff expected/all_areas.Area_Name.Devonshire.csv actual
#   diff expected/all_areas.Area_Name.Foothill.csv actual
#   diff expected/all_areas.Area_Name.Harbor.csv actual
#   diff expected/all_areas.Area_Name.Hollenbeck.csv actual
#   diff expected/all_areas.Area_Name.Hollywood.csv actual
#   diff expected/all_areas.Area_Name.Mission.csv actual
#   diff expected/all_areas.Area_Name.N_Hollywood.csv actual
#   diff expected/all_areas.Area_Name.Newton.csv actual
#   diff expected/all_areas.Area_Name.Northeast.csv actual
#   diff expected/all_areas.Area_Name.Olympic.csv actual
#   diff expected/all_areas.Area_Name.Pacific.csv actual
#   diff expected/all_areas.Area_Name.Rampart.csv actual
#   diff expected/all_areas.Area_Name.Southeast.csv actual
#   diff expected/all_areas.Area_Name.Southwest.csv actual
#   diff expected/all_areas.Area_Name.Topanga.csv actual
#   diff expected/all_areas.Area_Name.Van_Nuys.csv actual
#   diff expected/all_areas.Area_Name.West_LA.csv actual
#   diff expected/all_areas.Area_Name.West_Valley.csv actual
#   diff expected/all_areas.Area_Name.Wilshire.csv actual
# fi
# if [ ! -f "actual/draw_graph_2.out" ]; then
#   python ../pd.py scripts/draw_graph_2.txt > actual/draw_graph_2.out
#   mv *.csv actual
#   diff expected/draw_graph_2.out actual/draw_graph_2.out
#   diff expected/all_areas.Victim_Sex.F.csv actual
#   diff expected/all_areas.Victim_Sex.H.csv actual
#   diff expected/all_areas.Victim_Sex.M.csv actual
#   diff expected/all_areas.Victim_Sex.N.csv actual
#   diff expected/all_areas.Victim_Sex.X.csv actual
# fi
# node playground/ll_distance.js > actual/ll_distance.out
# diff expected/ll_distance.out actual
# if [ ! -f "actual/heat.out" ]; then
#   python ../pd.py scripts/heat.txt > actual/heat.out
#   diff expected/heat.out actual/heat.out
#   mv *.png actual
#   diff -b expected/Northeast.Hour.Victim_Sex.heatmap.png actual
#   diff -b expected/Northeast.Hour.Weekday.heatmap.png actual
#   diff -b expected/all_areas.Hour.Victim_Sex.heatmap.png actual
#   diff -b expected/all_areas.Hour.Weekday.heatmap.png actual
# fi