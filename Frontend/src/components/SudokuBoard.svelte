<script>
    export let board = [];
    export let editable = true;  // Initially the board is editable
    import { validateMove } from '../api.js';  // Import the API function
    let invalidCells = new Set(); // Track invalid cells as a set of row-col keys
    let message = '';  // Message to display

    async function handleInput(row, col, value) {
        if (editable) {
            const parsedValue = value ? parseInt(value, 10) : 0;
            const currentBoard = board.map(r => r.slice());  // Create a copy of the board before the change

            // Send the current board and the move to validateMove
            const isValid = await validateMove(currentBoard, [{ row, col, value: parsedValue }]);

            if (isValid) {
                board[row][col] = parsedValue;
                console.log(`Updated cell (${row}, ${col}) to ${parsedValue}`);

                // Create a new set to trigger reactivity
                const newInvalidCells = new Set(invalidCells);

                // If the move is valid, remove any invalid state
                if (parsedValue < 1 || parsedValue > 9 || !isValidMove(row, col, parsedValue)) {
                    newInvalidCells.add(`${row}-${col}`);
                } else {
                    newInvalidCells.delete(`${row}-${col}`);
                }

                // Check if any previously invalid cells become valid
                for (let cell of invalidCells) {
                    const [r, c] = cell.split('-').map(Number);
                    if (await validateMove(currentBoard, [{ row: r, col: c, value: board[r][c] }])) {
                        newInvalidCells.delete(cell);
                    }
                }
                invalidCells = newInvalidCells; // Assign the new set to trigger reactivity

                // Check if the board is complete and valid
                checkBoardCompletion();
            } else {
                console.log(`Invalid move at (${row}, ${col}) with value ${parsedValue}`);
                // Optionally, you can show an error message if the move is invalid
            }
        }
    }

    // Validate the move for Sudoku rules
    function isValidMove(row, col, value) {
        if (value < 1 || value > 9) return false;

        // Check row and column for duplicates
        for (let i = 0; i < 9; i++) {
            if (
                (board[row][i] === value && i !== col) || // Duplicate in the same row
                (board[i][col] === value && i !== row)    // Duplicate in the same column
            ) {
                return false;
            }
        }

        // Check 3x3 subgrid for duplicates
        const startRow = Math.floor(row / 3) * 3;
        const startCol = Math.floor(col / 3) * 3;
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                const currentRow = startRow + i;
                const currentCol = startCol + j;
                if (
                    board[currentRow][currentCol] === value &&
                    (currentRow !== row || currentCol !== col)
                ) {
                    return false;
                }
            }
        }

        return true;
    }

    // Check if the board is complete and valid
    function checkBoardCompletion() {
        let isComplete = true;
        let isValid = true;

        // Check if all cells are filled and if the board is valid
        for (let row = 0; row < 9; row++) {
            for (let col = 0; col < 9; col++) {
                if (board[row][col] === 0) {
                    isComplete = false;
                }
                if (!isValidMove(row, col, board[row][col])) {
                    isValid = false;
                }
            }
        }

        if (isComplete && isValid) {
            message = "Congratulations! You solved the puzzle!";
            editable = false;  // Make the board no longer editable
        }
    }
</script>

<div class="sudoku-container">
    <div class="sudoku-grid">
        {#each board as row, rowIndex}
            <div class="sudoku-row">
                {#each row as cell, colIndex}
                    <input
                        type="text"
                        value={cell || ''}
                        maxlength="1"
                        class="sudoku-cell"
                        class:invalid={invalidCells.has(`${rowIndex}-${colIndex}`)}
                        class:border-bottom={rowIndex % 3 === 2 && rowIndex !== 8}
                        class:border-right={colIndex % 3 === 2 && colIndex !== 8}
                        readonly={!editable}
                        on:input={(e) => {
                            const value = e.target.value;

                            if (value === '') {
                                // If the user deletes the input, set it to normal (clear invalid state)
                                const newInvalidCells = new Set(invalidCells);
                                newInvalidCells.delete(`${rowIndex}-${colIndex}`);
                                invalidCells = newInvalidCells;
                                handleInput(rowIndex, colIndex, value); // Set to normal state
                            } else if (value >= '1' && value <= '9') {
                                // Handle valid inputs (numbers 1-9)
                                handleInput(rowIndex, colIndex, parseInt(value, 10));
                            } else {
                                // If the input is invalid, don't write anything
                                e.target.value = ''; // Clear the input field
                            }
                        }}
                    />
                {/each}
            </div>
        {/each}
    </div>

    {#if message}
        <div class="congratulations-message">{message}</div>
    {/if}
</div>

<style>
    /* Styling for invalid cells */
    .sudoku-cell.invalid {
        background-color: #ffcccc;
        border-color: #ff0000;
    }

    /* Ensure the container fills the whole screen and is centered */
    .sudoku-container {
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #003300;
        flex-direction: column;  /* Align items vertically */
    }

    /* Define the grid layout with no gaps, ensuring rows and columns are tightly packed */
    .sudoku-grid {
        display: grid;
        grid-template-rows: repeat(9, 50px);
        grid-template-columns: repeat(9, 50px);
        max-width: 450px;
        max-height: 540px;
        width: 100%;
        height: 100%;
        border: 3px solid #00ff00;
        background-color: #003300;
        box-shadow: 0 0 20px #00ff00;
        grid-gap: 0;
    }

    /* Grid row and column style */
    .sudoku-row {
        display: contents;
    }

    /* Style for the individual Sudoku cells */
    .sudoku-cell {
        width: 100%;
        height: 100%;
        text-align: center;
        font-size: 1.4rem;
        font-weight: bold;
        color: #00ff00;
        background-color: #000;
        border: 1px solid #006400;
        outline: none;
        transition: all 0.3s;
        box-shadow: 0 0 5px #00ff00;
        margin: 0;
        padding: 0;
    }

    /* Focused cell style */
    .sudoku-cell:focus {
        background-color: #003300;
        box-shadow: 0 0 10px #00ff00;
    }

    /* Styling for invalid cells */
    .sudoku-cell.invalid {
        background-color: #ffcccc;
        border-color: #ff0000;
    }

    /* Styling for the bottom border of cells */
    .border-bottom {
        border-bottom: 3px solid #00ff00;
    }

    /* Styling for the right border of cells */
    .border-right {
        border-right: 3px solid #00ff00;
    }

    /* Styling for the congratulations message */
    .congratulations-message {
        color: #00ff00;
        font-size: 2rem;
        font-weight: bold;
        margin-top: 20px;
        text-align: center;
    }
</style>
