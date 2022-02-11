BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `testlar` (
	`testId`	INTEGER NOT NULL UNIQUE,
	`savol`	TEXT,
	`a`	TEXT,
	`b`	TEXT,
	`c`	TEXT,
	`d`	TEXT,
	`fanId`	INTEGER NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS `statistika` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`hodimId`	INTEGER NOT NULL UNIQUE,
	`fanid`	INTEGER NOT NULL UNIQUE,
	`test_soni`	INTEGER NOT NULL UNIQUE,
	`tj`	INTEGER UNIQUE,
	`sana`	TEXT
);
CREATE TABLE IF NOT EXISTS `hodimlar` (
	`hodimId`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Ism`	TEXT NOT NULL,
	`Familiyasi`	TEXT NOT NULL,
	`ish_joyi`	TEXT NOT NULL,
	`lavozimi`	TEXT NOT NULL,
	`parol`	TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `fanlar` (
	`fanId`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`fan_nomi`	TEXT
);
COMMIT;