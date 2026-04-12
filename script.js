let messageContainer = document.getElementById("message-container")
let messageInput = document.getElementById("message-input")
let sendBtn = document.getElementById("send-button");

const socket = io("http://localhost:3000");

let pkmTrainers = ["Harsh","Muskan","Pritanshu", "Priyanshi","Pragati"];
let username = pkmTrainers[Math.floor(Math.random() * pkmTrainers.length)];
appendMessage("You Joined The Chat", "right");
console.log(username);

socket.emit("new-user", username);

socket.on("user-connected", (user) => {
    appendMessage(user + ": joined the chat", "left" );
});


socket.on("user-disconnected", (user) => {
    appendMessage(user + "left the chat", "left");
});

socket.on("chat-message", (data) =>{
    console.log(data);
    appendMessage(data.user + ": " + data.data, "left");
});

// socket.emit("send-chat-message", "Eevee use tackle.");

sendBtn.addEventListener("click", e => {
    e.preventDefault()
    socket.emit("send-chat-message", messageInput.value)
    console.log(messageInput.value);
    appendMessage("You: " + messageInput.value, "right");
    messageInput.value = "";
})

function appendMessage(data, dir){
    let message = document.createElement("div");
    message.classList.add("message");
    message.classList.add(dir);
    message.textContent = data;
    messageContainer.append(message);
}

