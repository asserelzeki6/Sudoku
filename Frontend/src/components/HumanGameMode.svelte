<script>
    import SudokuBoard from './SudokuBoard.svelte';
    export let board;
    export let editable = true; // Allow editing in game mode

</script>

<SudokuBoard {board} {editable} />
