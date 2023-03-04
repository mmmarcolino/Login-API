use login_api;
CREATE TABLE users (username VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, surname VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, password BLOB NOT NULL, secure_auth INT, PRIMARY KEY (username));


