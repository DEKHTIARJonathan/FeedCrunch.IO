-- phpMyAdmin SQL Dump
-- version 4.5.5.1
-- http://www.phpmyadmin.net
--
-- Client :  localhost
-- Généré le :  Mer 23 Mars 2016 à 14:06
-- Version du serveur :  5.5.47-0+deb8u1-log
-- Version de PHP :  5.6.17-0+deb8u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Base de données :  `feedcrunch.io`
--

DELIMITER $$
--
-- Procédures
--
DROP PROCEDURE IF EXISTS `cleaning`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `cleaning` ()  MODIFIES SQL DATA
BEGIN 
      UPDATE `visits`  SET `ipAddress` = '172.21.159.208' WHERE  `ipAddress` = '172.21.159.208, 195.83.155.53';
      
      DELETE FROM `visits` WHERE `ipAddress` in (Select `ipAddress` FROM (select * from (SELECT `ipAddress`, count(*) as `c` FROM `visits` WHERE `webpage` LIKE "%?%" GROUP BY `ipAddress` ORDER BY `ipAddress`) as `t_temp` WHERE `t_temp`.`c` > 15 order by c DESC) as `t1`);
      
END$$

--
-- Fonctions
--
DROP FUNCTION IF EXISTS `get_domain`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `get_domain` (`link` VARCHAR(500) CHARSET utf8) RETURNS VARCHAR(500) CHARSET utf8 READS SQL DATA
BEGIN
DECLARE domain varchar(255);
SET domain = "";

SELECT CASE
      WHEN url RLIKE '^http://' THEN SUBSTRING_INDEX(SUBSTRING_INDEX(url, '/', 3), '/', -1)  
      WHEN url RLIKE '^https://' THEN SUBSTRING_INDEX(SUBSTRING_INDEX(url, '/', 3), '/', -1)
      ELSE SUBSTRING_INDEX(url, '/', 1) 
  END into domain
  FROM ( SELECT link AS url ) q;
  
  Return domain;
  
End$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Structure de la table `posts`
--
-- Création :  Mar 08 Mars 2016 à 22:20
--

DROP TABLE IF EXISTS `posts`;
CREATE TABLE `posts` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL DEFAULT '',
  `link` text NOT NULL,
  `when` varchar(16) NOT NULL DEFAULT '0000-00-00 00:00',
  `clicks` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Doublure de structure pour la vue `openedLinksCount`
--
DROP VIEW IF EXISTS `openedLinksCount`;
CREATE TABLE `openedLinksCount` (
`ipAddress` varchar(255)
,`vcount` bigint(21)
);

-- --------------------------------------------------------

--
-- Doublure de structure pour la vue `rssReaders`
--
DROP VIEW IF EXISTS `rssReaders`;
CREATE TABLE `rssReaders` (
`ipAddress` varchar(255)
,`vcount` bigint(21)
);

-- --------------------------------------------------------

--
-- Structure de la table `visitors`
--
-- Création :  Ven 19 Février 2016 à 13:10
--

DROP TABLE IF EXISTS `visitors`;
CREATE TABLE `visitors` (
  `ipAddress` varchar(255) NOT NULL,
  `visits` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `visits`
--
-- Création :  Mer 23 Mars 2016 à 13:53
--

DROP TABLE IF EXISTS `visits`;
CREATE TABLE `visits` (
  `ipAddress` varchar(255) NOT NULL,
  `timestamp` varchar(26) NOT NULL,
  `webpage` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la vue `openedLinksCount`
--
DROP TABLE IF EXISTS `openedLinksCount`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `openedLinksCount`  AS  select `visits`.`ipAddress` AS `ipAddress`,count(0) AS `vcount` from `visits` where (`visits`.`webpage` like '/post.php?postID=___') group by `visits`.`ipAddress` order by count(0) desc ;

-- --------------------------------------------------------

--
-- Structure de la vue `rssReaders`
--
DROP TABLE IF EXISTS `rssReaders`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `rssReaders`  AS  select `visits`.`ipAddress` AS `ipAddress`,count(0) AS `vcount` from `visits` where (`visits`.`webpage` = '/rss/index.php') group by `visits`.`ipAddress` order by count(0) desc ;

--
-- Index pour les tables exportées
--

--
-- Index pour la table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `visitors`
--
ALTER TABLE `visitors`
  ADD PRIMARY KEY (`ipAddress`);

--
-- Index pour la table `visits`
--
ALTER TABLE `visits`
  ADD PRIMARY KEY (`ipAddress`,`timestamp`),
  ADD KEY `timestamp` (`timestamp`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `posts`
--
ALTER TABLE `posts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=607;COMMIT;