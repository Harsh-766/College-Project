// let apiKey = "AIzaSyCO3V-NitIPpNMc-Arm7B_8gWgfVtynIE0"


import { GoogleGenerativeAI} from "@google/generative-ai";


const genAI = new GoogleGenerativeAI(import.meta.env.VITE_API_KEY);

const model = genAI.getGenerativeModel({
    model: "gemini-1.5-pro",
});

const generationConfig = {
    temperature:1,
    topP: 0.95,
    topK: 40,
    maxOutputTokens: 200,
    responseMimeType: "text/plain",
};

async function run(prompt) {
     const chatSession = model.startChat(
    {
        generationConfig,
        history:[
        ],
 });

    // const result = await chatSession.sendMessage(prompt);
    const result = await model.generateContent(prompt);
    return result.response.text()
}
 export default run;




