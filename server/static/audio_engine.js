//Static URLs
// TODO:: CHANGE THIS!!!!!
let WEB_SERVER_URL = "https://192.168.0.103:9091";

//
let previous_angle_string = "None, None, None, None";
let current_angle_string = "270, -15, 15, 130";

//global color state variable
let current_color   = "";
 
//function to start recording via r-pi
async function start_recording() {
    let url = WEB_SERVER_URL + "/start_recording"

    let result = await fetch(url, {
        method : "GET"
    });
 
    console.log("start recording request " + result);
    return 0;
}
 
//function to start recording via r-pi
async function stop_recording() {
    let url = WEB_SERVER_URL + "/stop_recording"
 
    let result = await fetch(url, {
        method : "GET"
    });
 
    console.log("stop recording request " + result);
    return 0;
}
 
//function to set the color of audio to serve
async function set_color_audio(requested_color) {
    let url = WEB_SERVER_URL + "/set_speaker_color";
    button_pressed = true; //debug color
 
    if (current_color == requested_color) {
        return 0;
    }
 
    await fetch(url, {
        "method": "POST",
        body: JSON.stringify({
            title: "color",
            body: requested_color,
        }),
        headers: {
            "Content-Type": "application/json",
        },
    });
 
    current_color = requested_color;

}
 
//function to receive the given audio color
async function get_angle_string() {
    //Stack over flow potential solution below
    let url = WEB_SERVER_URL + "/get_angles";
 
    let response = await fetch(url, { method: "GET" });
 
    body = response.body;
 
    let reader = body.getReader();
    let v = await reader.read();
    var received_angle_string = new TextDecoder().decode(v.value);
 
    // console.log("received file name = " + received_file_name);
 
    previous_angle_string = current_angle_string;
    current_angle_string = received_angle_string;
 
    console.log("previous angle = " + previous_angle_string);
    console.log("current angle  = " + current_angle_string);
 
    return 0;
}
