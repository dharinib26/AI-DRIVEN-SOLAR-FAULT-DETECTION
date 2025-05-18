-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 05, 2025 at 09:48 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `1solarfault`
--

-- --------------------------------------------------------

--
-- Table structure for table `activitytb`
--

CREATE TABLE `activitytb` (
  `id` bigint(10) NOT NULL auto_increment,
  `UserName` varchar(250) NOT NULL,
  `Date` varchar(250) NOT NULL,
  `Time` varchar(250) NOT NULL,
  `ObjectName` varchar(250) NOT NULL,
  `ActivityInfo` varchar(500) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `activitytb`
--

INSERT INTO `activitytb` (`id`, `UserName`, `Date`, `Time`, `ObjectName`, `ActivityInfo`) VALUES
(3, 'kalai', '2025-04-05', '15:12:47', 'faulty', 'static/upload/4293.jpg'),
(4, 'kalai', '2025-04-05', '15:17:31', 'faulty', 'static/upload/4682.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `regtb`
--

CREATE TABLE `regtb` (
  `id` bigint(10) NOT NULL auto_increment,
  `Name` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `EmailId` varchar(250) NOT NULL,
  `Address` varchar(500) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `regtb`
--

INSERT INTO `regtb` (`id`, `Name`, `Mobile`, `EmailId`, `Address`, `UserName`, `Password`) VALUES
(1, 'monisha', '9486365535', 'monisha@gmail.com', 'No 16, Samnath Plaza, Madurai Main Road, Melapudhur', 'monisha', 'monisha'),
(2, 'kalai', '8072906690', 'kalaiarasiboobalan@gmail.com', 'no 6 trcihy', 'kalai', 'kalai');
