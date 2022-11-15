# Chess
Functions:
  - Enpassant
  - Castle
  - All piece moves

Algoritmhs [depth 5 - 7]
  - Minimax
  - Negamax
  - Minimax [AlphaBeta pruning]
  - Negamax [AlphaBeta pruning]
  - Negamax [AlphaBeta pruning & transpositional tables]

Node Calculations [depth 3]
  - Negamax
    - 3.2
    - 13,016
  - Negamax [AB prune]
    - 0.5s
    - 2602
  - Negamax [AB prune | transposition table]
    - 0.07s
    - 297

Node Calculations [depth 4]
  - Negamax 
    - 95.5s
    - 374,830
  - Negamax [AB prune]
    - 4.8s
    - 17,309
  - Negamax [AB prune | transposition table]
    - 0.6s
    - 2,619
