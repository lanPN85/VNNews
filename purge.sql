USE `news_store`;
DELETE FROM articles WHERE id > 0;
ALTER TABLE articles AUTO_INCREMENT = 1;
