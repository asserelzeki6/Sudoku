<script>
    import SudokuBoard from './SudokuBoard.svelte';
    import { solvePuzzle } from '../api.js';

    export let board;
    export let editable = false;
    let moves = [];
    let moveIndex = 0; 
    let initialBoard = [...board]; 
    let solvedBoard = []; 
    let currentBoard = [...initialBoard]; 
    let isSolving = false; 
    let isSolved = false; 

    async function solveSudoku() {
        isSolving = true;
        solvePuzzle(board).then((response) => {
            console.log(response.board);
            solvedBoard = response.board; 
            currentBoard = [...solvedBoard]; 
            moves = response.moves; 
            moveIndex = moves.length - 1; 
            isSolved = true; 
        }).catch((error) => {
            console.error(error);
        }).finally(() => {
            isSolving = false;
        });
    }

    function nextMove() {
        if (moveIndex < moves.length - 1) {
            moveIndex += 1;
            applyMove(moves[moveIndex]);
        }
    }

    function prevMove() {
        if (moveIndex > 0) {
            revertMove(moves[moveIndex]);
            moveIndex -= 1;
        }
    }

    function getInitial() {
        //keep reverting moves until the first move
        while (moveIndex > 0) {
            prevMove();
        }
    }

    function getLast() {
        //keep applying moves until the last move
        while (moveIndex < moves.length - 1) {
            nextMove();
        }
    }

    function applyMove(move) {
        const [row, col, value] = move;
        currentBoard[row][col] = value; 
    }

    function revertMove(move) {
        const [row, col, value] = move;
        currentBoard[row][col] = 0; // Revert the move by setting the value to 0
    }
</script>

<div class="ai-game-mode">
    <h2>AI Player</h2>
    <div class="board-container">
        <SudokuBoard board={currentBoard} editable={false} />
    </div>
    
    <!-- Solve Button -->
    <button on:click={solveSudoku} disabled={isSolving || isSolved}>
        {#if isSolving}
            Solving...
        {/if}
        {#if !isSolving}
            Solve
        {/if}
    </button>
    
    <!-- Navigation Buttons -->
    <div class="move-controls">
        <button on:click={getInitial} disabled={moveIndex === 0 || !isSolved}>First</button>
        <button on:click={prevMove} disabled={moveIndex === 0 || !isSolved}>Previous</button>
        <button on:click={nextMove} disabled={moveIndex === moves.length - 1 || !isSolved}>Next</button>
        <button on:click={getLast} disabled={moveIndex === moves.length - 1 || !isSolved}>Last</button>
    </div>
</div>

<style>
    .ai-game-mode {
        display: flex;
        flex-direction: column;
        align-items: center;
        color: #00ff00;
    }

    .board-container {
        margin-bottom: 20px;
    }

    button {
        background-color: #00ff00;
        color: #000;
        border: none;
        font-size: 1.2rem;
        padding: 10px 20px;
        cursor: pointer;
        transition: background-color 0.3s;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
    }

    button:hover {
        background-color: #006400;
    }

    button:disabled {
        background-color: #cccccc;
        color: #666666;
        cursor: not-allowed;
    }

    .move-controls {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }

    .move-controls button {
        margin: 0 10px;
    }
</style>
