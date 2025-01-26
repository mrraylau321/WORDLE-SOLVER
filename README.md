# WORDLE-SOLVER

An automated solver for Wordle-like games that uses intelligent word filtering and character probability analysis.

## Acknowledgments

This project uses the English word list from [dwyl/english-words](https://github.com/dwyl/english-words) repository. Special thanks to the maintainers of this comprehensive word list.

## Features

- Multiple game modes support:
  - Daily word
  - Random word
  - Manual word input
- Smart word filtering based on game feedback
- Fallback mechanism for words outside standard dictionary
- Automatic retry for connection issues
- Uses comprehensive English word list from dwyl/english-words

## Requirements

- Python 3.7+
- Required packages in requirements.txt

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/mrraylau321/WORDLE-SOLVER.git
    cd WORDLE-SOLVER
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the solver:
    ```bash
    python src/wordle_solver.py
    ```

Follow the prompts to:
1. Choose game mode (daily/random/manual)
2. Enter word size (default: 5)
3. For manual mode, enter your target word

## Technical Implementation

### Word List Processing
- Fetches English words from dwyl/english-words repository
- Filters words based on target length
- Processes words to ensure lowercase and proper formatting

### Solving Algorithm
1. Initial Setup:
   - Creates numpy array for character tracking
   - Initializes word filtering system

2. Fallback Mechanism:
   - Handles cases where word isn't in standard list
   - Generates possible combinations based on known information

3. Error Handling:
   - Implements retry mechanism for API calls
   - Handles connection issues gracefully

## API Integration

Uses the Wordle API endpoints:
- /daily: For daily word challenges
- /random: For random word challenges
- /word/{word}: For custom word challenges

## License

This project is licensed under the MIT License.
