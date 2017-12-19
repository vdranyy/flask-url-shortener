PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE roles (
	id INTEGER NOT NULL, 
	name VARCHAR(64), 
	"default" BOOLEAN, 
	permissions INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (name), 
	CHECK ("default" IN (0, 1))
);
INSERT INTO "roles" VALUES(1,'Moderator',0,5);
INSERT INTO "roles" VALUES(2,'User',1,1);
INSERT INTO "roles" VALUES(3,'Administrator',0,255);
CREATE TABLE users (
	id INTEGER NOT NULL, 
	email VARCHAR(64), 
	username VARCHAR(64), 
	role_id INTEGER, 
	password_hash VARCHAR(128), 
	confirmed BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(role_id) REFERENCES roles (id), 
	CHECK (confirmed IN (0, 1))
);
INSERT INTO "users" VALUES(1,'suprophone@gmail.com','suprophone',2,'pbkdf2:sha256:50000$czkd4RYE$e2d75b83b475b79fff5ebf2e45488f0b200a51bda7ffa2eb3941e3f2887e2a9d',1);
CREATE TABLE urls (
	id INTEGER NOT NULL, 
	full_url TEXT, 
	short_url VARCHAR(64), 
	element_text TEXT, 
	clicks INTEGER, 
	created DATETIME, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
INSERT INTO "urls" VALUES(1,'http://www.nltk.org/book/','nltk','Natural Language Processing with Python&trade;. cool book and great',1,'2017-12-18 16:16:13.856086',NULL);
INSERT INTO "urls" VALUES(2,'https://mail.google.com/mail/u/0/#inbox','mail','One account. All of Google&trade;.',0,'2017-12-18 16:23:42.363588',NULL);
CREATE INDEX ix_roles_default ON roles ("default");
CREATE UNIQUE INDEX ix_users_email ON users (email);
CREATE UNIQUE INDEX ix_users_username ON users (username);
COMMIT;
