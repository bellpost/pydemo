/*
 Navicat Premium Data Transfer

 Source Server         : whbus
 Source Server Type    : SQLite
 Source Server Version : 3008004
 Source Database       : main

 Target Server Type    : SQLite
 Target Server Version : 3008004
 File Encoding         : utf-8

 Date: 09/29/2017 22:49:54 PM
*/

PRAGMA foreign_keys = false;

-- ----------------------------
--  Table structure for whbusstationinfo
-- ----------------------------
DROP TABLE IF EXISTS "whbusstationinfo";
CREATE TABLE "whbusstationinfo" (
	 "lineId" varchar(20,0),
	 "lineNo" varchar(10,0),
	 "stopId" varchar(20,0),
	 "stopName" varchar(64,0),
	 "stopNo" varchar(20,0),
	 "jingdu" DECIMAL(3,12),
	 "weidu" DECIMAL(3,12),
	 "orderId" int
);

PRAGMA foreign_keys = true;
