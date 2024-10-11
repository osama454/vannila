const express = require('express');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http);

const messages = []; // Store messages temporarily (in real app, use a database)

app.use(express.static(__dirname + '/public')); // Serve static files (HTML, CSS, JS)

io.on('connection', (socket) => {
    console.log('A user connected');
    socket.emit('initial_messages', messages); // Send chat history to new users

    socket.on('chat message', (msg) => {
        messages.push(msg); // Store the new message
        socket.broadcast.emit('chat message', msg); // Send to all other users
    });


    socket.on('disconnect', () => {
        console.log('User disconnected');
    });
});


http.listen(3000, () => {
    console.log('listening on *:3000');
});