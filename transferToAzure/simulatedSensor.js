/*
* IoT Hub Raspberry Pi NodeJS - Microsoft Sample Code - Copyright (c) 2017 - Licensed MIT
*/
'use strict';
var fs = require("fs");


function Sensor(/* options */) {
	
	console.log("Sensor initialized");
}

Sensor.prototype.init = function (callback) {
  // nothing todo
  callback();
}

Sensor.prototype.read = function (sensorData, callback) {

  	callback(null, {
		time: sensorData["time"],
		xa: sensorData["xa"],
		ya: sensorData["ya"],
		za: sensorData["za"],
    		xg: sensorData["xg"],
    		yg: sensorData["yg"],
		zg: sensorData["xg"]
  	});
}

function random(min, max) {
  return Math.random() * (max - min) + min;
}

module.exports = Sensor;
