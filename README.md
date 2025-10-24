# Left Recursion Elimination Algorithm

This project implements the left recursion elimination algorithm for Context-Free Grammars (CFG) as presented in Aho's Compilers book. The algorithm systematically removes both immediate and indirect left recursion from grammar productions.

---

##  Student Name

- **Andres Felipe Eusse Chavarria**




## OS Version

**Windows 10/11**


## Language and Libraries

- **Language:** Python 3
- **Libraries:**
  - **sys:** Standard library for:
    - `sys.argv`: Command-line argument handling
    - `sys.stdin`: Input stream management
  - **io:** Standard library for:
    - `io.StringIO`: String buffer manipulation for input redirection

---



## How the Algorithm Works

This algorithm implements a three-stage sequential process to eliminate left recursion, based on the standard methodology from the Aho textbook.

## Phase 1: Ordering and Setup
First, all non-terminals are organized into a fixed order ($A_1, A_2, ..., A_n$). Establishing this sequence is essential for methodically resolving both indirect and immediate left recursion. The system also tracks existing non-terminal names to ensure any newly generated symbols are unique.

## Phase 2: Iterative Substitution
This is the core loop of the algorithm. It iterates through each non-terminal $A_i$ in the established order.For each $A_i$, it checks its productions against all preceding non-terminals $A_j$ (where $j < i$).If a production like $A_i \to A_j\gamma$ is found, the algorithm replaces $A_j$ with all of its corresponding productions.This crucial step systematically converts any indirect left recursion into immediate left recursion.

## Phase 3: Immediate Recursion Elimination
Finally, the algorithm processes each non-terminal that now has immediate left recursion.Productions matching the pattern: $A \to A\alpha_1 | A\alpha_2 | ... | A\alpha_m | \beta_1 | \beta_2 | ... | \beta_n$ (where $\beta$ terms do not start with A)Are rewritten into two new sets of rules:$A \to \beta_1A' | \beta_2A' | ... | \beta_nA'$$A' \to \alpha_1A' | \alpha_2A' | ... | \alpha_mA' | \varepsilon$This transformation introduces a new non-terminal (A') to manage the recursive part, effectively eliminating all left recursion from the grammar.

## Key Features
Dual Operation:

Command-line (CLI) mode for direct input.

Interactive mode for a guided, step-by-step process.

Versatile: Capable of handling both simple and complex grammars with numerous productions.

Reliable: Automatically generates new, conflict-free non-terminal names.

Clear Output: Formats the results legibly, separating the original grammar from the transformed one.

Batch Mode: Can process a file containing multiple grammars in a single run.

## How to Run
Method 1: CLI Argument
Run the script by passing the grammar as a string argument:

PowerShell

python run_prueba.py "A -> Aa | b"
Method 2: Interactive Session
Start the script without arguments to enter interactive mode:

PowerShell

python run_prueba.py
Then, follow the prompts to enter your grammar.

## Method 3: File Pipelining
Prepare Your File Create a file input.txt with the structure specified below.

Run the Command

PowerShell

Get-Content input.txt | python run_prueba.py

## Input File Structure
The input.txt file (for Method 3) must follow this format:

Line 1: The total number of grammars (n) to process.

For each grammar:

First line: The number of non-terminals (k) in that grammar.

Next k lines: The productions, in the format: NonTerminal -> production1 | production2 | ...

## Sample Input File
Plaintext

2
1
A -> Aa | b
2
S -> Sa | Sb | c
E -> E+T | T
📤 Corresponding Output
Plaintext

A -> bB
B -> aB | e

S -> cC
C -> aC | bC | e
E -> TD
D -> +TD | e

 ## Grammar Syntax
 When writing a grammar (either in CLI or interactive mode), use this format:

Use -> to separate the non-terminal (left side) from its productions (right side).

Use | to separate alternative production rules for the same non-terminal.

Example: A -> Aa | Ab | c

## Reference
Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). Compilers: Principles, Techniques, and Tools (2nd ed.). Addison-Wesley.
