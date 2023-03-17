DROP TABLE IF EXISTS Covalent_Token_Event;
-- DROP TABLE IF EXISTS Address;

CREATE TABLE IF NOT EXISTS STAGING.Covalent_Token_Event (
        id serial NOT NULL PRIMARY KEY
      , data jsonb NOT NULL
      , page integer NOT NULL
);


