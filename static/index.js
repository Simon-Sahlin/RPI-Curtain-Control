
let slider = document.querySelector("#slider > input")
let curtainPos = document.querySelector("#slider > div:nth-child(1) > input[type=number]")
let maxPos = document.querySelector("#slider > div:nth-child(3) > input[type=number]")

let times = [
    document.querySelector("#weekControls > div:nth-child(1) > input"),
    document.querySelector("#weekControls > div:nth-child(2) > input"),
    document.querySelector("#weekControls > div:nth-child(3) > input"),
    document.querySelector("#weekControls > div:nth-child(4) > input"),
    document.querySelector("#weekControls > div:nth-child(5) > input"),
    document.querySelector("#weekControls > div:nth-child(6) > input"),
    document.querySelector("#weekControls > div:nth-child(7) > input"),
    document.querySelector("#mainInputs > div:nth-child(2) > input"),
]
let tomorrowTime = document.querySelector("#mainInputs > div:nth-child(1) > input");

let upButt = document.querySelector("#up")
let stopButt = document.querySelector("#stop")
let downButt = document.querySelector("#down")


function getState(){
    return {
        sliderPos: slider.value,
        currentPos: curtainPos.value,
        maxPos: maxPos.value,
        times: times.map(a => a.value)
    }
}

async function updateState(){
    let state = getState();
    let res = await fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(state),
    });

    if (res.ok) {
        console.log('State updated');
        console.log(state)
    } else {
        console.log('State update failed');
    }
}

async function sendAction(action){
    let res = await fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(action),
    });

    if (res.ok) {
        console.log('Action sent');
        console.log(action)
    } else {
        console.log('Action failed');
    }
}


/* ------------------------------------ - ----------------------------------- */

upButt.addEventListener('click', () => sendAction({
    action: "moveTo",
    value: 0
}));

downButt.addEventListener('click', () => sendAction({
    action: "moveTo",
    value: maxPos.value
}));

stopButt.addEventListener('click', () => sendAction({
    action: "stop"
}));

slider.addEventListener('change', () => {
    curtainPos.value = slider.value;
    sendAction({
        action: "moveTo",
        value: slider.value
    });
});

curtainPos.addEventListener('change', () =>{
    slider.value = curtainPos.value;
    sendAction({
        action: "moveTo",
        value: curtainPos.value
    });
});

maxPos.addEventListener('change', () => {
    slider.max = maxPos.value;
    updateState();
});

times.forEach((time)=>{
    time.addEventListener('change', updateState)
});

tomorrowTime.addEventListener('change', () => {
    let weekday = (new Date()).getDay()
    times[weekday].value = tomorrowTime.value
    updateState();
})