
const modelParams = {
    flipHorizontal: true,   // flip e.g for video 
    imageScaleFactor: 2,  // reduce input image size for gains in speed.
    maxNumBoxes: 2,        // maximum number of boxes to detect
    iouThreshold: 0.1,      // ioU threshold for non-max suppression
    scoreThreshold: 0.6,    // confidence threshold for predictions.
  }

const video = document.querySelector('#video');
const canvas = document.querySelector('#canvas');
const context = canvas.getContext('2d');
let model;

handTrack.startVideo(video).then(status => {
    if (status) {
        navigator.getUserMedia(
            { video: {} },
            stream => {
                setInterval(runDetection,5)
            },
            err => console.log(err)
        );
    }
});

function runDetection(){
    model.detect(video).then(predictions => {
        try {
            console.log(predictions[0].bbox)
            websocket.send(`{"action": "position", "predictions": "${predictions[0].bbox}"}`);
            websocket.send(`{"action": "position", "predictions": "${predictions[1].bbox}"}`);
        } catch (error) {
            
        }
        model.renderPredictions(predictions, canvas, context, video);
    })
}

handTrack.load(modelParams).then(lmodel => {
    model = lmodel;
})


var users = document.querySelector('.users'),
                websocket = new WebSocket("ws://127.0.0.1:6788");

websocket.onmessage = function (event) {
    data = JSON.parse(event.data);
    switch (data.action) {
        case 'connected':
            console.log("Connected")
            break;
        default:
            console.error(
                "unsupported event", data);
    }
};