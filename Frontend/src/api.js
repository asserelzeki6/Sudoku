const BASE_URL = 'http://localhost:5000/api/game'; // Replace with your Flask backend URL

// Utility function to handle JSON POST requests
async function postRequest(endpoint, data) {
    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

// Utility function to handle GET requests
async function getRequest(endpoint) {
    try {
        const response = await fetch(`${BASE_URL}${endpoint}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        console.log(response);
        return response.json();
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

// Function to get an easy Sudoku puzzle
export async function getEasyPuzzle() {
    return getRequest('/easy');
}

// Function to get a medium Sudoku puzzle
export async function getMediumPuzzle() {
    return getRequest('/medium');
}

// Function to get a hard Sudoku puzzle
export async function getHardPuzzle() {
    return getRequest('/hard');
}

// Function to validate the input Sudoku board
export async function validateInput(board) {
    return postRequest('/validate_input', { board });
}

// Function to validate a move on the Sudoku board
export async function validateMove(board, move) {
    return postRequest('/validate_move', { board, move });
}

// Function to solve the Sudoku puzzle
export async function solvePuzzle(board) {
    return postRequest('/solve', { board });
}
