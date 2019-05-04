/*
* IoT Hub Raspberry Pi NodeJS - Microsoft Sample Code - Copyright (c) 2017 - Licensed MIT
*/
'use strict';
var fs = require("fs");

const Bme280Sensor = require('./bme280Sensor.js');
const SimulatedSensor = require('./simulatedSensor.js');

function MessageProcessor(option) {
  option = Object.assign({
    deviceId: '[Unknown device] node',
    temperatureAlert: 30
  }, option);
  this.sensor = option.simulatedData ? new SimulatedSensor() : new Bme280Sensor(option.i2cOption);
  this.deviceId = option.deviceId;
  this.temperatureAlert = option.temperatureAlert
  this.sensor.init(() => {
    this.inited = true;
  });
  this.sensorData = JSON.parse(fs.readFileSync('data.json', 'utf8'));
  this.readIndex = -1;
}

MessageProcessor.prototype.getMessage = function (messageId, cb) {
  if (!this.inited) { return; }
  this.readIndex += 1;
  var strIndex = this.readIndex.toString()
  this.sensor.read(this.sensorData[strIndex], (err, data) => {
    if (err) {
      console.log('[Sensor] Read data failed: ' + err.message);
      return;
    }

    cb(JSON.stringify({
      	messageId: messageId,
      	deviceId: this.deviceId,
	time: data.time,
	xa: data.xa,
	ya: data.ya,
	za: data.za,
    	xg: data.xg,
    	yg: data.yg,
	zg: data.zg
    }), data.temperature > this.temperatureAlert);
  });
}

module.exports = MessageProcessor;
