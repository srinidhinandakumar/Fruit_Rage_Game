# Fruit_Rage_Game
The goal is to develop a smart AI agent based on Alpha Beta Prunning that accurately chooses the cell in the input matrix, whose selction will help it gain maximum points.

It is similar to Candy Crush where a fruit of type=1 is chosen, all neighboring cells with fruit type=1 are collected. 
The score then is given as count_fruits_collected^2.

Once a fruit is chosen and the cell is empty - fruits above fall down as an effect of gravity.

`gameplay.py` plays `AI_Agent.py` against a Random Agent, Minimax Agent (that explores depth no greater than 3) and an Alpha Beta Agent.
