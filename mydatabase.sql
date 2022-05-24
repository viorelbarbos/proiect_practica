-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 24, 2022 at 07:07 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mydatabase`
--

-- --------------------------------------------------------

--
-- Table structure for table `facedetection`
--

CREATE TABLE `facedetection` (
  `id` int(12) UNSIGNED NOT NULL,
  `NumePrenume` varchar(20) NOT NULL,
  `NrMatricol` varchar(12) NOT NULL,
  `locatieImagine` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `facedetection`
--

INSERT INTO `facedetection` (`id`, `NumePrenume`, `NrMatricol`, `locatieImagine`) VALUES
(1, 'Barbos Viorel', '98', 'db_img\\viorel.jpg'),
(2, 'Sofron Vasile', '99', 'db_img\\vasile.jpg'),
(3, 'Crainic Rares', '97', 'db_img\\rares.jpg'),
(4, 'Danciu Silvia', '96', 'db_img\\silvia.jpg'),
(5, 'Dumitras Andrei', '95', 'db_img\\andrei.jpg'),
(6, 'Pasca Emanuel', '94', 'db_img\\emanuel.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `tabelprezenta`
--

CREATE TABLE `tabelprezenta` (
  `id` int(11) NOT NULL,
  `NumePrenume` varchar(20) NOT NULL,
  `NrMatricol` varchar(12) NOT NULL,
  `Prezenta` tinyint(1) DEFAULT 0,
  `Data` date NOT NULL,
  `LocatieImagine` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='TP';

--
-- Dumping data for table `tabelprezenta`
--

INSERT INTO `tabelprezenta` (`id`, `NumePrenume`, `NrMatricol`, `Prezenta`, `Data`, `LocatieImagine`) VALUES
(1, 'Barbos Viorel', '98', 1, '2022-05-02', ''),
(2, 'Sofron Vasile', '99', 0, '2022-05-02', ''),
(3, 'Crainic Rares', '97', 0, '2022-05-02', ''),
(4, 'Danciu Silvia', '96', 0, '2022-05-02', ''),
(5, 'Dumitras Andrei', '95', 0, '2022-05-02', ''),
(6, 'Pasca Emanuel', '94', 0, '2022-05-02', ''),
(7, 'Barbos Viorel', '98', 1, '2022-05-21', '2022-05-21\\Barbos Viorel.jpg'),
(8, 'Sofron Vasile', '99', 0, '2022-05-21', ''),
(9, 'Crainic Rares', '97', 0, '2022-05-21', ''),
(10, 'Danciu Silvia', '96', 0, '2022-05-21', ''),
(11, 'Dumitras Andrei', '95', 0, '2022-05-21', ''),
(12, 'Pasca Emanuel', '94', 0, '2022-05-21', ''),
(13, 'Barbos Viorel', '98', 1, '2022-05-22', '2022-05-22\\Barbos Viorel.jpg'),
(14, 'Sofron Vasile', '99', 0, '2022-05-22', ''),
(15, 'Crainic Rares', '97', 0, '2022-05-22', ''),
(16, 'Danciu Silvia', '96', 0, '2022-05-22', ''),
(17, 'Dumitras Andrei', '95', 0, '2022-05-22', ''),
(18, 'Pasca Emanuel', '94', 0, '2022-05-22', ''),
(19, 'Barbos Viorel', '98', 1, '2022-05-22', '2022-05-22\\Barbos Viorel.jpg'),
(20, 'Sofron Vasile', '99', 0, '2022-05-22', ''),
(21, 'Crainic Rares', '97', 0, '2022-05-22', ''),
(22, 'Danciu Silvia', '96', 0, '2022-05-22', ''),
(23, 'Dumitras Andrei', '95', 0, '2022-05-22', ''),
(24, 'Pasca Emanuel', '94', 0, '2022-05-22', ''),
(25, 'Barbos Viorel', '98', 1, '2022-05-22', '2022-05-22\\Barbos Viorel.jpg'),
(26, 'Sofron Vasile', '99', 0, '2022-05-22', ''),
(27, 'Crainic Rares', '97', 0, '2022-05-22', ''),
(28, 'Danciu Silvia', '96', 0, '2022-05-22', ''),
(29, 'Dumitras Andrei', '95', 0, '2022-05-22', ''),
(30, 'Pasca Emanuel', '94', 0, '2022-05-22', ''),
(31, 'Barbos Viorel', '98', 1, '2022-05-23', '2022-05-23\\Barbos Viorel.jpg'),
(32, 'Sofron Vasile', '99', 0, '2022-05-23', ''),
(33, 'Crainic Rares', '97', 0, '2022-05-23', ''),
(34, 'Danciu Silvia', '96', 0, '2022-05-23', ''),
(35, 'Dumitras Andrei', '95', 0, '2022-05-23', ''),
(36, 'Pasca Emanuel', '94', 0, '2022-05-23', ''),
(37, 'Barbos Viorel', '98', 1, '2022-05-24', '2022-05-24\\Barbos Viorel.jpg'),
(38, 'Sofron Vasile', '99', 1, '2022-05-24', '2022-05-24\\Sofron Vasile.jpg'),
(39, 'Crainic Rares', '97', 1, '2022-05-24', '2022-05-24\\Crainic Rares.jpg'),
(40, 'Danciu Silvia', '96', 0, '2022-05-24', ''),
(41, 'Dumitras Andrei', '95', 1, '2022-05-24', '2022-05-24\\Dumitras Andrei.jpg'),
(42, 'Pasca Emanuel', '94', 1, '2022-05-24', '2022-05-24\\Pasca Emanuel.jpg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `facedetection`
--
ALTER TABLE `facedetection`
  ADD PRIMARY KEY (`id`),
  ADD KEY `nr_matricol` (`NrMatricol`);

--
-- Indexes for table `tabelprezenta`
--
ALTER TABLE `tabelprezenta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `nr_mat` (`NrMatricol`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `facedetection`
--
ALTER TABLE `facedetection`
  MODIFY `id` int(12) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `tabelprezenta`
--
ALTER TABLE `tabelprezenta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
