## Propositional Calculus Prover

The prover takes an S-Expression and returns whether it is a:
* Tautology, returns `T`
* Satisfiable, returns `Number` saying how many times it is `True`
* Unsatisfiable, returns `U`
* Invalid S-Espression, returns `E`

### Example Of Propositional Calculus
```
p -> q: Means If p then q, 
which translated into propositional calculus gives: (~p OR q)  
``` 

A Truth Table for the above example looks like this:

| p | q |~p | q | ~p OR q (p -> q)|
|---|---|---|---|--------|
| F | F | T | F |    T   |
| F | T | T | T |    T   |
| T | F | F | F |    F   |
| T | T | F | T |    T   |


### Supported Operations:
* NOT
* OR
* IF
* AND


### TODO:
* Support **IFF**
* Refactor to make it more modular