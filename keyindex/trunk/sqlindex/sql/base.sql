-- Table: contentclass2resource

-- DROP TABLE contentclass2resource;

CREATE TABLE contentclass2resource
(
  id int8 NOT NULL,
  content_class text NOT NULL,
  name text NOT NULL,
  CONSTRAINT PK_contentclass2resource_id PRIMARY KEY (id)
) 
WITHOUT OIDS;

-- Index: "class"

-- DROP INDEX "class";

CREATE INDEX IX_contentclass2resource_class
  ON contentclass2resource
  USING btree
  (content_class);

-- Index: name

-- DROP INDEX name;

CREATE INDEX IX_contentclass2resource_name
  ON contentclass2resource
  USING btree
  (name);

-- Table: "keyindex_indexValues"

-- DROP TABLE "keyindex_indexValues";

CREATE TABLE keyindexvalues
(
  id int8 NOT NULL,
  title text NOT NULL,
  searchabletext text NOT NULL,
  subject text NOT NULL,
  description text NOT NULL,
  created timestamp,
  modified timestamp,
  contenttype text NOT NULL,
  creators text NOT NULL,
  CONSTRAINT PK_keyindexvalues_id PRIMARY KEY (id)
) 
WITHOUT OIDS;

-- Index: "searchableText"

-- DROP INDEX "searchableText";

CREATE INDEX IX_keyindexvalues_searchabletext
  ON keyindexvalues
  USING btree
  (searchabletext);

-- Index: subject

-- DROP INDEX subject;

CREATE INDEX IX_keyindexvalues_subject
  ON keyindexvalues
  USING btree
  (subject);

-- Index: title

-- DROP INDEX title;

CREATE INDEX IX_keyindexvalues_title
  ON keyindexvalues
  USING btree
  (title);

-- Index: description

-- DROP INDEX description;

CREATE INDEX IX_keyindexvalues_description
  ON keyindexvalues
  USING btree
  (title);

-- Index: created

-- DROP INDEX created;

CREATE INDEX IX_keyindexvalues_created
  ON keyindexvalues
  USING btree
  (title);

-- Index: modified

-- DROP INDEX modified;

CREATE INDEX IX_keyindexvalues_modified
  ON keyindexvalues
  USING btree
  (modified);

-- Index: "contentType"

-- DROP INDEX "contentType";

CREATE INDEX IX_keyindexvalues_contenttype
  ON keyindexvalues
  USING btree
  (contenttype);