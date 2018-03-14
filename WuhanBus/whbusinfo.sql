/*
 Navicat Premium Data Transfer

 Source Server         : whbus
 Source Server Type    : SQLite
 Source Server Version : 3008004
 Source Database       : main

 Target Server Type    : SQLite
 Target Server Version : 3008004
 File Encoding         : utf-8

 Date: 09/29/2017 22:49:46 PM
*/

PRAGMA foreign_keys = false;

-- ----------------------------
--  Table structure for whbusinfo
-- ----------------------------
DROP TABLE IF EXISTS "whbusinfo";
CREATE TABLE "whbusinfo" (
	 "lineId" varchar(20,0) NOT NULL,
	 "lineNo" varchar(10,0),
	 "lineName" varchar(10,0),
	 "direction" int,
	 "endStopName" varchar(64,0),
	 "startStopName" varchar(64,0),
	 "firstTime" varchar(10,0),
	 "lastTime" varchar(10,0),
	 "stopsNum" int,
	PRIMARY KEY("lineId")
);

PRAGMA foreign_keys = true;
