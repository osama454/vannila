const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// In-memory user store
const inMemoryUsers = {};

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));

// Serve the homepage with links to signup and signin
app.get('/', (req, res) => {
    res.send(`
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Home</title>
        </head>
        <body>
            <h1>Welcome to the Authentication App</h1>
            <a href="/signup">Sign Up</a><br>
            <a href="/signin">Sign In</a>
        </body>
        </html>
    `);
});

// Signup route (GET and POST)
app.get('/signup', (req, res) => {
    res.send(`
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Sign Up</title>
        </head>
        <body>
            <h1>Sign Up</h1>
            <form action="/signup" method="POST">
                <label for="username">Username:</label>
                <input type="text" name="username" required><br><br>
                <label for="password">Password:</label>
                <input type="password" name="password" required><br><br>
                <button type="submit">Sign Up</button>
            </form>
            <a href="/">Go Back</a>
        </body>
        </html>
    `);
});

app.post('/signup', (req, res) => {
    const { username, password } = req.body;

    if (inMemoryUsers[username]) {
        return res.send(`
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Sign Up</title>
            </head>
            <body>
                <h1>Username already exists. Please try another one.</h1>
                <a href="/signup">Go back to Sign Up</a>
            </body>
            </html>
        `);
    }

    // Store new user
    inMemoryUsers[username] = password;
    res.redirect('/signin');
});

// Signin route (GET and POST)
app.get('/signin', (req, res) => {
    res.send(`
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Sign In</title>
        </head>
        <body>
            <h1>Sign In</h1>
            <form action="/signin" method="POST">
                <label for="username">Username:</label>
                <input type="text" name="username" required><br><br>
                <label for="password">Password:</label>
                <input type="password" name="password" required><br><br>
                <button type="submit">Sign In</button>
            </form>
            <a href="/">Go Back</a>
        </body>
        </html>
    `);
});

app.post('/signin', (req, res) => {
    const { username, password } = req.body;

    // Check if the user exists and the password matches
    if (inMemoryUsers[username] && inMemoryUsers[username] === password) {
        res.send(`
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Welcome</title>
            </head>
            <body>
                <h1>Hello, ${username}</h1>
                <a href="/">Go Back to Home</a>
            </body>
            </html>
        `);
    } else {
        res.send(`
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Sign In</title>
            </head>
            <body>
                <h1>Invalid username or password. Please try again.</h1>
                <a href="/signin">Go back to Sign In</a>
            </body>
            </html>
        `);
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
