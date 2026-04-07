import React, { createContext, useState } from "react"
import run from '../gemini';
export const datacontext = createContext()
function UserContext({children}){
let [speaking,setSpeaking] = useState(false)
let [prompt,setPrompt] = useState("listening...")
let [response,setResponse] = useState(false)
    function speak(text){
let text_speak = new SpeechSynthesisUtterance(text)
text_speak.volume = 1;
text_speak.rate = 1;
text_speak.pitch = 1;
text_speak.lang = "hi-GB"
window.speechSynthesis.speak(text_speak)
    }

async function aiResponse(prompt) {
    let text=await run(prompt)
    let newText = text.split("**")&&text.split("*")&&text.replace("google","Harsh")&&text.replace("Google", "Harsh")
    setPrompt(newText)
    speak(newText)
    setResponse(true);
    setTimeout(()=>{
        setSpeaking(false)
    },4000)
    // setSpeaking(false)
}
let speechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = new speechRecognition();
recognition.onresult=(e) => {
let currentIndex=e.resultIndex
let transcript=e.results[currentIndex][0].transcript
setPrompt(transcript)
takeCommand(transcript.toLowerCase())
}

function takeCommand (command){
    if(command.includes("open") && command.includes("youtube")){
        window.open("https://www.youtube.com/", "_blank")
        speak("opening Youtube")
        setPrompt("opening Youtube...")
        setTimeout(()=>{
          setSpeaking(false)
           },4000)
    }
     else if(command.includes("open") && command.includes("google")){
        window.open("https://www.google.com/", "_blank")
        speak("opening google")
        setResponse(true)
        setPrompt("opening google...")
        setTimeout(()=>{
          setSpeaking(false)
           },4000)
    }
    else if(command.includes("open") && command.includes("whatsapp")){
        window.open("https://web.whatsapp.com/", "_blank")
        speak("opening whatsApp")
        setResponse(true)
        setPrompt("opening whatsApp...")
        setTimeout(()=>{
          setSpeaking(false)
           },4000)
    }
     else if(command.includes("open") && command.includes("netflix")){
        window.open("https://www.netflix.com/in/", "_blank")
        speak("opening netflix")
        setResponse(true)
        setPrompt("opening netflix...")
        setTimeout(()=>{
          setSpeaking(false)
           },4000)
    }
     else if(command.includes("open") && command.includes("flipkart")){
        window.open("https://www.flipkart.com/", "_blank")
        speak("opening flipkart")
        setResponse(true)
        setPrompt("opening flipkart...")
        setTimeout(()=>{
          setSpeaking(false)
           },4000)
    }
     else if(command.includes("open") && command.includes("github")){
        window.open("https://github.com/", "_blank")
        speak("opening github")
        setResponse(true)
        setPrompt("opening github...")
        setTimeout(()=>{
          setSpeaking(false)
           },4000)
    }
     else if(command.includes("open") && command.includes("cuims")){
        window.open("https://uims.cuchd.in/", "_blank")
        speak("opening cuims")
        setResponse(true)
        setPrompt("opening cuims...")
        setTimeout(()=>{
          setSpeaking(false)
           },4000)
    }
     else if(command.includes("time")){
         let time = new Date().toLocaleString(undefined,
            {hour:"numeric",minute:"numeric"})
        speak(time)
        setResponse(true)
        setPrompt(time)
        setTimeout(()=>{
          setSpeaking(false)
           },4000)
    }
     else if(command.includes("date")){
         let date = new Date().toLocaleString(undefined,
            {day:"numeric", month:"short",year:"numeric"})
        speak(date)
        setResponse(true)
        setPrompt(date)
        setTimeout(()=>{
          setSpeaking(false)
           },4000)
    }
    
    else {
        aiResponse(command)
    }
}
    let value={
     recognition,
     speaking,
     setSpeaking,
     prompt,
     setPrompt,
     response,
     setResponse
    }
    return (
        <div>
        <datacontext.Provider value={value}>
            {children}
        </datacontext.Provider>
        </div>
    )
}

export default UserContext;