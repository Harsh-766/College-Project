const io = require("socket.io") (3000,{
    cors: {
        origin:"*",
    },
});

console.log("Socket.IO server running on http://localhost:3000");

let users = {};

io.on("connection", (socket) => {
    console.log(socket.id);
    socket.on("new-user", (user) => {
        users[socket.id] = user;
        // console.log(user);
        socket.broadcast.emit("user-connected", user);
    });
   
    socket.on("send-chat-message", (data) => {
        // console.log(data);
         socket.broadcast.emit("chat-message",{user: users[socket.id], data});
    });

    socket.on("disconnect", () => {
        socket.broadcast.emit("user-disconnected", users[socket.id])
        delete users[socket.id];
    })
});