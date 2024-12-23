export async function generatePuzzle(difficulty) {
    const res = await fetch(`/api/generate?difficulty=${difficulty}`);
    return res.json();
}

export async function solvePuzzle(board) {
    const res = await fetch('/api/solve', {
        method: 'POST',
        body: JSON.stringify({ board }),
        headers: { 'Content-Type': 'application/json' }
    });
    return res.json();
}

export async function validateBoard(board) {
    const res = await fetch('/api/validate', {
        method: 'POST',
        body: JSON.stringify({ board }),
        headers: { 'Content-Type': 'application/json' }
    });
    const result = await res.json();
    return result.isValid;
}
