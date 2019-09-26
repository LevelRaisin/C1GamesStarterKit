$scriptPath = Split-Path -parent $PSCommandPath;
$algoPath = "$scriptPath\\algo_strategy_maze_raptor.py"

python $algoPath
