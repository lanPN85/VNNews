CREATE DATABASE news_store;
CREATE TABLE articles (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NOT NULL,
  `referer` varchar(256) DEFAULT NULL,
  `title` varchar(512) DEFAULT NULL,
  `intro` text,
  `content` mediumtext,
  `domain` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `url_UNIQUE` (`url`)
) ENGINE=InnoDB AUTO_INCREMENT=3392 DEFAULT CHARSET=utf8;
