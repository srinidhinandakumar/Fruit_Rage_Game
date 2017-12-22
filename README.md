# Fruit_Rage_Game
The goal is to develop a smart AI agent based on Alpha Beta Prunning that accurately chooses the cell in the input matrix, whose selction will help it gain maximum points.

It is similar to Candy Crush where a fruit of type=1 is chosen, all neighboring cells with fruit type=1 are collected. 
The score then is given as count_fruits_collected^2.

Once a fruit is chosen and the cell is empty - fruits above fall down as an effect of gravity.

`gameplay.py` plays `AI_Agent.py` against a Random Agent, Minimax Agent (that explores depth no greater than 3) and an Alpha Beta Agent.

### Example
20 `number n for nxn matrix`
5 `number of types of fruits p (0 - (p-1))`
300 `number of seconds left to complete game`
22134113013333023311
34300430203323211434
41141222332103434314
21320232421024421332
32113311431430432212
23313212331211021131
11213313233301101121
21031023130142412322
20211322321223303234
03322213111003202200
13440434142302213414
42342023101042103441
40323210344442222323
11034332131223121102
01303112212401111023
33132131310122202202
42324141320233222313
21133431321140322410
44241311221232331132
33123241104421321210
