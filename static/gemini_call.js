let stream = null;

const video = document.getElementById("video");
const status = document.getElementById("status");
const answer = document.getElementById("answer");

let liveMode = false;
let visionTimer = null;


document.getElementById("startBtn").onclick = async()=>{

    stream = await navigator.mediaDevices.getUserMedia({
        video:true
    });


    video.srcObject = stream;


    status.innerText =
    "Camera running";


    startLiveVision();

};



async function sendFrame(){

    const canvas=document.createElement("canvas");


    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;


    const ctx=canvas.getContext("2d");


    ctx.drawImage(
        video,
        0,
        0
    );


    const image=canvas.toDataURL(
        "image/jpeg",
        0.7
    );


    status.innerText =
    "Sending to Gemini...";


    const response = await fetch(
        "/gemini_camera",
        {
            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                image:image
            })
        }
    );


    const data = await response.json();


    answer.innerText =
    data.reply;

    if(data.reply){

        const voice = await fetch(
            "/voice",
            {
                method:"POST",
                headers:{
                    "Content-Type":"application/json"
                },
                body:JSON.stringify({
                    text:data.reply
                })
            }
        );
    
    
        const audioBlob =
        await voice.blob();
    
    
        const audioURL =
        URL.createObjectURL(audioBlob);
    
    
        const audio =
        new Audio(audioURL);
    
    
        audio.play();
    
    }


    status.innerText =
    "👁️ Watching";

}



function startLiveVision(){

    if(liveMode)
        return;


    liveMode=true;


    status.innerText =
    "👁️ Live vision started";


    visionTimer=setInterval(()=>{

        if(video.videoWidth > 0){

            sendFrame();

        }

    },5000);

}



function stopLiveVision(){

    liveMode=false;


    clearInterval(
        visionTimer
    );


    status.innerText =
    "Live vision stopped";

}