BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `tests` (
	`test_id`	INTEGER NOT NULL UNIQUE,
	`question`	TEXT,
	`a`	TEXT,
	`b`	TEXT,
	`c`	TEXT,
	`d`	TEXT,
	`fan_id`	INTEGER NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS `subjects` (
	`subject_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`subject_name`	TEXT
);
CREATE TABLE IF NOT EXISTS `statistics` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`employe_id`	INTEGER NOT NULL UNIQUE,
	`subject_id`	INTEGER NOT NULL UNIQUE,
	`count`	INTEGER NOT NULL UNIQUE,
	`answers`	INTEGER UNIQUE,
	`date`	TEXT
);
CREATE TABLE IF NOT EXISTS `employees` (
	`employe_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT NOT NULL,
	`surname`	TEXT NOT NULL,
	`workplace`	TEXT NOT NULL,
	`position`	TEXT NOT NULL,
	`password`	TEXT NOT NULL
);
COMMIT;
