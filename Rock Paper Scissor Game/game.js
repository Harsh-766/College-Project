let userScore = 0;
let compScore = 0;

const choices = document.querySelectorAll(".choice");
const msg = document.querySelector("#msg");
const userScorepara = document.querySelector("#user-score");
const compScorepara = document.querySelector("#comp-score");

const genComp = () => {
    const option = ["rock","paper","scissors"];
    const randIndx = Math.floor(Math.random()*3);
    return option [randIndx];
};

const drawGame = () => {
    // console.log("game draw!");
    msg.innerText = "Game Draw";
     msg.style.backgroundColor = "#081b31";
};

const showWinner = (userWin) => {
    if(userWin){
        // console.log("You Win");
        userScore++;
        userScorepara.innerText = userScore;
        msg.innerText = "You Win";
        msg.style.backgroundColor = "green";
    } else {
        // console.log("You Lose");
        compScore++;
        compScorepara.innerText = compScore;
        msg.innerText = "You Lose";
         msg.style.backgroundColor = "red";
    }
}

const playGame = (userChoice) => {
    // console.log("user choices =",userChoice);
    const compChoice = genComp();
    // console.log("comp choice = ",compChoice);

    if (userChoice === compChoice) {
        drawGame();
    } else{
        let userWin = true;
        if(userChoice === "rock"){
            userWin = compChoice === "paper" ? false : true;
        } else if(userChoice === "paper"){
            userWin = compChoice === "scissors" ? false : true;
        } else {
            userWin = compChoice === "rock" ? false : true;
        }
        showWinner(userWin);
    }
};


choices.forEach((choice) => {
    choice.addEventListener("click",() => {
        const userChoice = choice.getAttribute("id");
        playGame(userChoice);
    });
});
