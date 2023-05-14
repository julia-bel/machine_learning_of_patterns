# Machine learning of patterns

> ### Basic algorithms
> - Lange and Wiehagen's pattern language learning algorithm: https://www.researchgate.net/publication/2464047.
> - Angluin's pattern language learning algorithm: https://www.sciencedirect.com/science/article/pii/0022000080900410.

## Algorithm
1) Let $L = \{ l_1, ..., l_k \}$ be the ascending set of unique lengths of all dataset words.
2) Sequentially apply the Lange and Wiehagen's algorithm to the set of words of length $l_1, ..., l_k$.
3) If the pattern inclusion condition isn't satisfied, then apply the Angluin's algorithm to these patterns.
4) The result pattern corresponds to the minimum length words.

<p align="center">
    <img src="assets/algorithm.svg" width="896" height="504" alt="Learning algorithm"/>
</p>

## Installing
```
git clone https://github.com/julia-bel/machine_learning_of_patterns
pip install -r requirements.txt
```

## Learning
```
python main.py [-h] -d DATASET_PATH [-o] 
```

```-d, --dataset_path``` - path to the file with words for learning (default ```datasets/dataset.csv```).          
```-o, --optimize``` - whether to use optimization of Angluin's algorithm.


## File structure
```
.
|-- README.md
|-- assets
|   `-- readme visualizations
|-- automaton
|   |-- abstract_automaton.py - superclass for NFA and DFA
|   `-- automaton.py - implementation of NFA and DFA for regex matching
|-- datasets
|   `-- files with datasets
|-- experiments 
|   |-- matching_time.ipynb - notebook with time measurements
|   |-- two_steps_generation.ipynb - notebook for dataset creating
|   `-- dataset.csv - dataset regexes
|-- learning_algorithm
|   |-- angluin_learning.py - implementation of Angluin's algorithm
|   `-- lange_weihagen_learning.py - implementation of LWA
|-- pattern
|   |-- abstract_pattern.py - superclass for non-erasing pattern
|   `-- pattern.py - implementation of non-erasing pattern
|-- regex
|   |-- abstract_regex.py - superclass for regex 
|   |-- const.py - constants for regex module
|   |-- generator.py - generator of random regex
|   |-- parser.py - regex parser
|   `-- regex.py - implementation of regex
|-- utils
|   `-- utils.py - common utilities
|-- visualization
|   `-- *.gv, *.gv.png files for DFA, NFA and regex structure visualization
|-- requirements.txt
`-- main.py - script for patterns learning
```
