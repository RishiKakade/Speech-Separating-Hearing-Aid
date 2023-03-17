
let recButton;
let stopButton;

let redButton;
let blueButton;
let orangeButton;
let greenButton;

let titleFont;
let bodyFont;

let titleFontSize;
let bodyFontSize;
let smallBodyFontSize;

let currRecording = false;

let start_button_clicked = false;
let stop_button_clicked = false;

let red_button_clicked = false;
let blue_button_clicked = false;
let orange_button_clicked = false;
let green_button_clicked = false;

let bgColorIndex = 0;

// Colours must be defined in functions - require p5js library
let darkRed;
let darkBlue;
let darkOrange;
let darkGreen;

let red;
let blue;
let orange;
let green;

let bgRed;
let bgBlue;
let bgOrange;
let bgGreen;

let white;
let black;

// Dimension constants
let recButtonWidth;
let recButtonHeight;
let buffer;
let recButtonPos;
let titleVerticalPos;
let speakerButtonWidth;
let speakerButtonHeight;

let posImageWidth;
let posImageHeight;

let paused = false;

function preload() {
	titleFont = loadFont("./fonts/BungeeShade-Regular.ttf");
	bodyFont = loadFont("./fonts/Jost-ExtraLight.ttf");
}

function setup() {
	frameRate(60);
	createCanvas(windowWidth, windowHeight);
}

function draw() {
    //get_angle_string();
    // audio_logic_loop();
	
	darkRed = color(189, 93, 21);
	darkBlue = color(1, 87, 128);
	darkOrange = color(171, 139, 14);
	darkGreen = color(44, 99, 42);
	darkStopRed = color(176, 39, 0);

	red = color(226, 135, 67);
	blue = color(30, 129, 176);
	orange = color(255, 204, 0);
	green = color(76, 168, 72);
	stopRed = color(255, 55, 0);

	bgGrey = color(240, 240, 240);
	bgRed = color(252, 216, 189);
	bgBlue = color(211, 234, 245);
	bgOrange = color(252, 234, 164);
	bgGreen = color(231, 252, 230);
	
	white = color(255, 255, 255);
	black = color(0, 0, 0);

	const bgColor = [bgGrey, bgRed, bgBlue, bgOrange, bgGreen];
	
	// Array to handle updating background color
	titleFontSize = windowHeight/12;
	bodyFontSize = windowHeight/25;
	smallBodyFontSize = windowHeight/35;
	
	// Dimensions
	buffer = windowHeight/60;
	textFont(bodyFont);
	textSize(bodyFontSize);
	let maxTextWidth = textWidth("Stop Recording");
	titleVerticalPos = windowHeight/8;
	recButtonWidth = Math.min(maxTextWidth + 4*buffer, (windowWidth - 50));
	recButtonHeight = windowHeight/13;
	recButtonPos = [(windowWidth - recButtonWidth)/2, titleVerticalPos + titleFontSize/2];
	speakerButtonWidth = (recButtonWidth - buffer)/2;
	speakerButtonHeight = recButtonHeight;
	
	// Positions image
	posImageWidth = recButtonWidth;
	posImageHeight = posImageWidth * (480/640);	// original png: 640x480 pixels

	background(bgColor[bgColorIndex]);

	const speakerButtonLeft = (windowWidth - recButtonWidth)/2;
	const speakerButtonRight = (windowWidth + recButtonWidth)/2;
	const speakerButtonTop = recButtonPos[1] + 2*buffer + posImageHeight + smallBodyFontSize + 1.5*speakerButtonHeight;
	const speakerButtonBottom = speakerButtonTop + buffer + speakerButtonHeight;
	
	fill(black);
	stroke(black);
	textFont(titleFont);
	textAlign(CENTER);
	textSize(titleFontSize);

	if (textWidth('LISTENX') > 1.2*recButtonWidth) {
		textSize(0.85*titleFontSize);
	}

	let title = text('LISTENX', windowWidth/2, titleVerticalPos);
	title.uxStrokeWeight = 0;
	
	if (currRecording === false) {
		// Start recording button
		uxFill(blue);
		uxStroke(darkBlue);
		recButton = uxRect(recButtonPos[0], recButtonPos[1], recButtonWidth, recButtonHeight);
		recButton.uxEvent('click', recButtonClick);
		// recButton.uxStrokeWeight = 3;
		recButton.uxRender();
		
		fill(white);
		stroke(white);
		textFont(bodyFont);
		textSize(bodyFontSize);
		recButtonText = text('Start Recording', windowWidth/2, titleVerticalPos + titleFontSize + recButtonHeight/2.5 - bodyFontSize/2);
		recButtonText.uxStrokeWeight = 0;
	}
	else {
		uxFill(red);
		uxStroke(darkRed);
		redButton = uxRect(speakerButtonLeft, speakerButtonTop, speakerButtonWidth, speakerButtonHeight);
		redButton.uxEvent('click', redButtonClick);
		// redButton.uxStrokeWeight = 3;

		uxFill(blue);
		uxStroke(darkBlue);
		blueButton = uxRect(speakerButtonRight - speakerButtonWidth, speakerButtonTop, speakerButtonWidth, speakerButtonHeight);
		blueButton.uxEvent('click', blueButtonClick);
		// blueButton.uxStrokeWeight = 3;

		
		uxFill(orange);
		uxStroke(darkOrange);
		orangeButton = uxRect(speakerButtonLeft, speakerButtonBottom, speakerButtonWidth, speakerButtonHeight);
		orangeButton.uxEvent('click', orangeButtonClick);
		// orangeButton.uxStrokeWeight = 3;

		
		uxFill(green);
		uxStroke(darkGreen);
		greenButton = uxRect(speakerButtonRight - speakerButtonWidth, speakerButtonBottom, speakerButtonWidth, speakerButtonHeight);
		greenButton.uxEvent('click', greenButtonClick);
		// greenButton.uxStrokeWeight = 3;


		// Stop recording button
		uxFill(stopRed);
		uxStroke(darkStopRed);
		const stopButtonHeight = speakerButtonBottom + buffer + speakerButtonHeight + smallBodyFontSize;
		stopButton = uxRect((windowWidth - recButtonWidth)/2, stopButtonHeight, recButtonWidth, recButtonHeight);
		stopButton.uxEvent('click', stopButtonClick);
		// stopButton.uxStrokeWeight = 3;

		// Render buttons before text (under text)
		stopButton.uxRender();
		redButton.uxRender();
		blueButton.uxRender();
		orangeButton.uxRender();
		greenButton.uxRender();
		
		fill(white);
		stroke(white);
		textFont(bodyFont);
		textSize(bodyFontSize);
		const stopButtonTextHeight = recButtonPos[1] + posImageHeight + 2*speakerButtonHeight + recButtonHeight/2.5 + bodyFontSize/2 + 6*buffer + smallBodyFontSize + 1.5*speakerButtonHeight;
		stopButtonText = text('Stop Recording', windowWidth/2, stopButtonTextHeight);
		
		textAlign(LEFT);
		textSize(smallBodyFontSize);
		fill(blue);
		stroke(blue);
		const chooseSpeakerTextHeight = recButtonPos[1] + 2*buffer + posImageHeight + smallBodyFontSize/2;
		// choseSpeakerText = text('Choose Speaker:', (windowWidth - recButtonWidth)/2, chooseSpeakerTextHeight);
		draw_speaker_animation(windowWidth/2, (titleVerticalPos + titleFontSize + speakerButtonTop)/2 - speakerButtonHeight/2,recButtonWidth);
	}
}

function windowResized() {
	resizeCanvas(windowWidth, windowHeight);
}

function recButtonClick() {

	//checking if button clicked flag is active
	if(start_button_clicked == true) {
		return 0;
	}
	
	//resetting button clicked flags
	start_button_clicked 	= true;
	stop_button_clicked 	= false;

	red_button_clicked 		= false;
	blue_button_clicked 	= false;
	orange_button_clicked 	= false;
	green_button_clicked 	= false;

	currRecording = true;
	bgColorIndex = 0;
	start_recording();
}

function stopButtonClick() {

	//checking if button clicked flag is active
	if(stop_button_clicked == true) {
		return 0;
	}
	
	//resetting button clicked flags
	start_button_clicked 	= false;
	stop_button_clicked 	= true;

	red_button_clicked 		= false;
	blue_button_clicked 	= false;
	orange_button_clicked 	= false;
	green_button_clicked 	= false;

	currRecording = false;
	bgColorIndex = 0;
	stop_recording();
}

function redButtonClick() {
	if (!currRecording) {
		return 0;
	}

	//checking if button clicked flag is active
	if(red_button_clicked == true) {
		return 0;
	}
	
	//resetting button clicked flags
	start_button_clicked 	= false;
	stop_button_clicked 	= false;

	red_button_clicked 		= true;
	blue_button_clicked 	= false;
	orange_button_clicked 	= false;
	green_button_clicked 	= false;

	bgColorIndex = 1;
	set_color_audio("red");
}

function blueButtonClick() {
	if (!currRecording) {
		return 0;
	}

	//checking if button clicked flag is active
	if(blue_button_clicked == true) {
		return 0;
	}
	
	//resetting button clicked flags
	start_button_clicked 	= false;
	stop_button_clicked 	= false;

	red_button_clicked 		= false;
	blue_button_clicked 	= true;
	orange_button_clicked 	= false;
	green_button_clicked 	= false;
	
	bgColorIndex = 2;
	set_color_audio("blue");
}

function orangeButtonClick() {
	if (!currRecording) {
		return 0;
	}

	//checking if button clicked flag is active
	if(orange_button_clicked == true) {
		return 0;
	}
	
	//resetting button clicked flags
	start_button_clicked 	= false;
	stop_button_clicked 	= false;

	red_button_clicked 		= false;
	blue_button_clicked 	= false;
	orange_button_clicked 	= true;
	green_button_clicked 	= false;
	
	bgColorIndex = 3;
	set_color_audio("orange");
}

function greenButtonClick() {
	if (!currRecording) {
		return 0;
	}

	//checking if button clicked flag is active
	if(green_button_clicked == true) {
		return 0;
	}
	
	//resetting button clicked flags
	start_button_clicked 	= false;
	stop_button_clicked 	= false;

	red_button_clicked 		= false;
	blue_button_clicked 	= false;
	orange_button_clicked 	= false;
	green_button_clicked 	= true;
	
	bgColorIndex = 4;
+	set_color_audio("green");
}

//best_color = color(135,62,35);
