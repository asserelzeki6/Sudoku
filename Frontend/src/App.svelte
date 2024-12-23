<script>
    import { writable } from 'svelte/store';
    import SudokuBoard from './components/SudokuBoard.svelte';
    import GameMode from './components/GameMode.svelte'; // Import the GameMode component

    const mode = writable('home');
    let randomBoard = generateRandomBoard();
    let playerType = writable('human');
    let generationMode = writable('easy');
    let customBoard = false;

    function generateRandomBoard() {
        return [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ];
    }
	function generateEmptyBoard()
	{
		return [
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
	}
    // Function to reset the board to an empty state
    function resetBoard() {
        randomBoard = generateEmptyBoard(); // Reset to an empty board
    }
    function changePlayerType(type) {
		console.log("Player type changed to: " + type);
        playerType.set(type);
    }

    function changeGenerationMode(mode) {
        generationMode.set(mode);
        if (mode === 'custom') {
            customBoard = true;
        } else {
            customBoard = false;
            randomBoard = generateRandomBoard();
        }
    }

    function confirmCustomBoard() {
        console.log("Custom board confirmed.");
    }

    function startGame() {
        mode.set('game'); // Set the mode to 'game' to show the game screen
    }

    function goBack() {
        mode.set('home'); // Set the mode back to 'home' to return to the main menu
    }
</script>
<div class="theme">
    <h1>Welcome to Sudoku</h1>

    <div class="container">
        <div class="board-container">
            {#if $mode === 'home'}
                <SudokuBoard board={randomBoard} editable={customBoard} />
            {/if}

            {#if $mode === 'game'}
                <GameMode board={randomBoard} editable={$playerType === 'human'} />
            {/if}
        </div>

        <div class="menu" class:hide={$mode === 'game'}>
            <div class="game-controls">
                <h2>Select Player</h2>
                <button on:click={() => changePlayerType('human')} class={$playerType === 'human' ? 'selected' : ''}>Human Player</button>
                <button on:click={() => changePlayerType('ai')} class={$playerType === 'ai' ? 'selected' : ''}>AI Player</button>

                <h2>Select Game Mode</h2>
                <div class="game-mode-grid">
                    <button on:click={() => changeGenerationMode('easy')} class={$generationMode === 'easy' ? 'selected' : ''}>Easy</button>
                    <button on:click={() => changeGenerationMode('med')} class={$generationMode === 'med' ? 'selected' : ''}>Medium</button>
                    <button on:click={() => changeGenerationMode('hard')} class={$generationMode === 'hard' ? 'selected' : ''}>Hard</button>
                    <button on:click={() => changeGenerationMode('custom')} class={$generationMode === 'custom' ? 'selected' : ''}>Custom</button>
                </div>

                {#if customBoard}
                    <button on:click={confirmCustomBoard}>Confirm Custom Board</button>
					<button on:click={resetBoard} class="reset-button">Reset Board</button>

                {/if}
                
            </div>
        </div>

        <!-- Start Game Button centered -->
        {#if $mode === 'home'}
            <div class="start-button-container">
                <button on:click={startGame} class="start-button">Start Game</button>
            </div>
        {/if}

        <!-- Back Button in game mode -->
        {#if $mode === 'game'}
            <div class="back-button-container">
                <button on:click={goBack} class="back-button">Back</button>
            </div>
        {/if}
    </div>
</div>


<style>
    html, body {
        height: 100%;
        margin: 0;
        padding: 0;
        overflow: hidden;
    }

    .theme {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        height: 100%;
        font-family: 'Courier New', monospace;
        color: #00ff00;
        background-color: #020d02;
    }

    .container {
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        width: 90%;
        max-width: 1000px;
        background-color: #003300;
        padding: 20px;
        border: 3px solid #020802;
        box-shadow: 0 0 20px #031003;
    }

    .menu {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: flex-start;
        width: 250px;
        padding: 20px;
        margin-right: 20px;
    }

    .game-controls {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }

    .game-mode-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr); /* 2 columns */
        gap: 10px;
        width: 100%;
    }

    .board-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    button {
        background-color: #006400;
        color: #00ff00;
        border: none;
        font-size: 1rem;
        padding: 10px;
        margin: 10px;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    button:hover {
        background-color: #00ff00;
        color: #000;
    }

    .selected {
        background-color: #00ff00;
        color: #000;
    }

    h1 {
        color: #00ff00;
        text-shadow: 0 0 10px #00ff00;
        margin-bottom: 20px;
    }

    h2 {
        color: #00ff00;
        text-shadow: 0 0 10px #00ff00;
    }

    .start-button-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }

    .start-button {
        background-color: #00ff00;
        color: #000;
        border: none;
        font-size: 1.2rem;  /* Smaller font size */
        padding: 10px 20px; /* Smaller padding */
        cursor: pointer;
        transition: background-color 0.3s, transform 0.2s;
        border-radius: 8px; /* Slightly smaller border radius */
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.5); /* Smaller shadow */
    }

    .start-button:hover {
        background-color: #006400;
        transform: scale(1.05); /* Slightly smaller scale effect */
    }

    .start-button:active {
        background-color: #004d00;
        transform: scale(1);
    }

    .back-button-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-top: 40px;
    }

    .back-button {
        background-color: #ff0000;
        color: #fff;
        border: none;
        font-size: 1.2rem;  /* Smaller font size */
        padding: 10px 20px; /* Smaller padding */
        cursor: pointer;
        transition: background-color 0.3s, transform 0.2s;
        border-radius: 8px; /* Slightly smaller border radius */
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.5); /* Smaller shadow */
    }

    .back-button:hover {
        background-color: #cc0000;
        transform: scale(1.05); /* Slightly smaller scale effect */
    }

    .back-button:active {
        background-color: #990000;
        transform: scale(1);
    }

    .hide {
        display: none;
    }

	.reset-button {
        background-color: #cc0000;
        color: #fff;
        border: none;
        font-size: 1rem;
        padding: 10px;
        margin: 10px;
        cursor: pointer;
        transition: background-color 0.3s;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
    }

    .reset-button:hover {
        background-color: #ff6666;
    }

    .reset-button:active {
        background-color: #ff3333;
    }
</style>
