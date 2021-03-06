PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE todo (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, target TEXT NOT NULL, name TEXT NOT NULL, description TEXT , status INTEGER NOT NULL DEFAULT 0, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL);
INSERT INTO "todo" VALUES(1,'DB schema','Add support for ON DELETE and ON UPDATE','',1,'2016-12-03 21:41:03');
INSERT INTO "todo" VALUES(2,'Source code','Add support for translations','',0,'2016-12-03 21:41:03');
INSERT INTO "todo" VALUES(3,'/location/modify/TestLocation1','Result message of location modify is ugly','',0,'2016-12-03 21:41:03');
INSERT INTO "todo" VALUES(4,'/location/add','Result message of location add is too simple','',0,'2016-12-03 21:41:03');
INSERT INTO "todo" VALUES(5,'/box/show/','Add link to location information','',0,'2016-12-03 21:41:03');
INSERT INTO "todo" VALUES(6,'/box/add','Result message of box add is too simple','',0,'2016-12-03 21:41:03');
INSERT INTO "todo" VALUES(7,'Source code','When using status, variable name should be status_id','',0,'2016-12-03 21:41:03');
INSERT INTO "todo" VALUES(8,'/box/modify/','Validate occypancy as number 0..100','',0,'2016-12-03 21:41:03');
INSERT INTO "todo" VALUES(9,'/box/modify/','Resule message of box modify is too simple','',0,'2016-12-03 21:41:03');
INSERT INTO "todo" VALUES(10,'/location/modify','Validate all input fields','',0,'2016-12-03 21:41:03');
INSERT INTO "todo" VALUES(11,'/box/modify','Validate all input fields','',0,'2016-12-03 21:41:03');
INSERT INTO "todo" VALUES(12,'/item/modify','Validate all input fields','',0,'2016-12-03 21:41:03');
INSERT INTO "todo" VALUES(13,'/location/add','Validate all input fields','',0,'2016-12-03 21:41:03');
INSERT INTO "todo" VALUES(14,'/box/add','Validate all input fields','',0,'2016-12-03 21:41:03');
INSERT INTO "todo" VALUES(15,'/item/add','Validate all input fields','',0,'2016-12-03 21:41:03');
INSERT INTO "todo" VALUES(16,'Source code','Create simple TODO functionality','',2,'2016-12-03 21:41:03');
INSERT INTO "todo" VALUES(17,'/item/add','Implement functionality','',2,'2016-12-03 21:41:03');
INSERT INTO "todo" VALUES(18,'/item/modify','Implement functionality','',1,'2016-12-03 21:41:03');
INSERT INTO "todo" VALUES(19,'HIAPP','Add functionaity to add new tasks','',0,'2016-12-03 21:59:51');
INSERT INTO "todo" VALUES(20,'/login','Add logint password check for all pages','',0,'2016-12-03 22:05:51');
DELETE FROM sqlite_sequence;
INSERT INTO "sqlite_sequence" VALUES('todo',20);
COMMIT;
