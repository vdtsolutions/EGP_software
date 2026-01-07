-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 17, 2020 at 10:01 AM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mfldata`
--

-- --------------------------------------------------------

--
-- Table structure for table `defectdetail`
--

CREATE TABLE `defectdetail` (
  `runid` int(10) DEFAULT NULL,
  `pipe_id` int(10) DEFAULT NULL,
  `defect_id` int(10) NOT NULL,
  `defect_length` float DEFAULT NULL,
  `defect_breadth` float DEFAULT NULL,
  `defect_angle` int(10) DEFAULT NULL,
  `defect_depth` int(10) DEFAULT NULL,
  `type` varchar(10) NOT NULL,
  `x` float NOT NULL,
  `y` float NOT NULL,
  `category` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `defectdetail`
--

INSERT INTO `defectdetail` (`runid`, `pipe_id`, `defect_id`, `defect_length`, `defect_breadth`, `defect_angle`, `defect_depth`, `type`, `x`, `y`, `category`) VALUES
(5, 8, 21, 8, 5, 0, 0, 'system', 8, 39, 'internal'),
(5, 8, 22, 2, 43, 0, 0, 'manual', 3, 20, 'unknown');

-- --------------------------------------------------------

--
-- Table structure for table `pipedetail`
--

CREATE TABLE `pipedetail` (
  `runid` int(1) DEFAULT NULL,
  `analytic_id` int(1) DEFAULT NULL,
  `pipe_id` int(1) NOT NULL,
  `pipe_start_filename` int(1) DEFAULT NULL,
  `pipe_start_serialno` int(1) DEFAULT NULL,
  `pipe_end_filename` int(1) DEFAULT NULL,
  `pipe_end_serialno` int(1) DEFAULT NULL,
  `pipe_length` float NOT NULL,
  `lower_sensitivity` float NOT NULL,
  `upper_sensitivity` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `pipedetail`
--

INSERT INTO `pipedetail` (`runid`, `analytic_id`, `pipe_id`, `pipe_start_filename`, `pipe_start_serialno`, `pipe_end_filename`, `pipe_end_serialno`, `pipe_length`, `lower_sensitivity`, `upper_sensitivity`) VALUES
(5, 1, 4, 1, 0, 1, 20, 0, 0, 1),
(1, 1, 5, 1, 0, 1, 114323, 0, 0, 0),
(3, 1, 6, 1, 0, 1, 40728, 0, 0, 0),
(4, 1, 7, 1, 0, 1, 159427, 0, 0, 0),
(5, 1, 8, 1, 0, 1, 20, 0, 0, 1),
(5, 1, 9, 1, 0, 1, 20, 0, 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `projectdetail`
--

CREATE TABLE `projectdetail` (
  `runid` int(5) NOT NULL,
  `ProjectName` varchar(20) DEFAULT NULL,
  `Pipeline_owner` varchar(50) DEFAULT NULL,
  `Pipeline_Name` varchar(50) DEFAULT NULL,
  `Launch` varchar(50) DEFAULT NULL,
  `Receive` varchar(50) DEFAULT NULL,
  `Diameter` float DEFAULT NULL,
  `Length` float DEFAULT NULL,
  `Steel_grade` varchar(50) DEFAULT NULL,
  `Nominal_wall` varchar(50) DEFAULT NULL,
  `Pipe_type` varchar(50) DEFAULT NULL,
  `MAOP_entry` varchar(50) DEFAULT NULL,
  `Design_pressure` varchar(50) DEFAULT NULL,
  `Defect_Assessment` varchar(50) DEFAULT NULL,
  `Year_of_commissioning` varchar(4) DEFAULT NULL,
  `Inspection_history` varchar(20) DEFAULT NULL,
  `Pipeline_product` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `projectdetail`
--

INSERT INTO `projectdetail` (`runid`, `ProjectName`, `Pipeline_owner`, `Pipeline_Name`, `Launch`, `Receive`, `Diameter`, `Length`, `Steel_grade`, `Nominal_wall`, `Pipe_type`, `MAOP_entry`, `Design_pressure`, `Defect_Assessment`, `Year_of_commissioning`, `Inspection_history`, `Pipeline_product`) VALUES
(1, 'vdt', 'dfg', 'bh', 'ccv', 'nnn', 0, 0, 'ccvvv', 'vvvv', 'dddvvbb', 'bb', 'ccc', 'fff', 'fff', 'vvv', 'vbc'),
(2, 'vdt1', 'ewdjje', 'mdm', 'dnd', 'ndn', 0, 0, 'dnfn', 'ndnf', 'bdb', 'ndn', 'dnf', 'ndbf', 'dbfb', 'dbfb', 'xyz'),
(3, 'vdt2', 'dffb', 'whehe', 'ndsn', 'dnn', 0, 0, 'ndcdn', 'ndsn', 'snd', 'sdbd', 'bsxdb', 'ndsn', 'cdn', 'nsdns', 'dsbd'),
(4, 'vdt3', 'sxbx', 'mxsmx', 'msm', 'msms', 0, 0, 'sxns', 'msx', 'msx', 'msx', 'mmxs', 'sxm', 'sns', 'sxsss', 'sns'),
(5, 'vdt4', '', '', '', '', 0, 0, '', '', '', '', '', '', '', '', ''),
(6, 'vdt5', '', '', '', '', 0, 0, '', '', '', '', '', '', '', '', ''),
(7, 'vdt6', '', '', '', '', 0, 0, '', '', '', '', '', '', '', '', ''),
(8, 'vdt7', '', '', '', '', 0, 0, '', '', '', '', '', '', '', '', ''),
(9, 'vdt8', '', '', '', '', 0, 0, '', '', '', '', '', '', '', '', ''),
(10, 'vdt9', '', '', '', '', 0, 0, '', '', '', '', '', '', '', '', ''),
(11, 'ajlk', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(21, 'a large project name', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `idUsers,UserName,Password` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`idUsers,UserName,Password`) VALUES
('1,sanjay,sanjay');

-- --------------------------------------------------------

--
-- Table structure for table `welddetail`
--

CREATE TABLE `welddetail` (
  `runid` int(1) DEFAULT NULL,
  `analytic_id` int(2) DEFAULT NULL,
  `Sensitivity` decimal(2,1) DEFAULT NULL,
  `weld_id` int(2) NOT NULL,
  `weld_start_filename` int(1) DEFAULT NULL,
  `weld_start_serialno` int(1) DEFAULT NULL,
  `weld_end_filename` int(1) DEFAULT NULL,
  `weld_end_serialno` int(1) DEFAULT NULL,
  `weld_length` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `welddetail`
--

INSERT INTO `welddetail` (`runid`, `analytic_id`, `Sensitivity`, `weld_id`, `weld_start_filename`, `weld_start_serialno`, `weld_end_filename`, `weld_end_serialno`, `weld_length`) VALUES
(5, 1, '9.9', 5, 1, 0, 1, 20, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `defectdetail`
--
ALTER TABLE `defectdetail`
  ADD PRIMARY KEY (`defect_id`);

--
-- Indexes for table `pipedetail`
--
ALTER TABLE `pipedetail`
  ADD PRIMARY KEY (`pipe_id`);

--
-- Indexes for table `projectdetail`
--
ALTER TABLE `projectdetail`
  ADD PRIMARY KEY (`runid`);

--
-- Indexes for table `welddetail`
--
ALTER TABLE `welddetail`
  ADD PRIMARY KEY (`weld_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `defectdetail`
--
ALTER TABLE `defectdetail`
  MODIFY `defect_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `pipedetail`
--
ALTER TABLE `pipedetail`
  MODIFY `pipe_id` int(1) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `projectdetail`
--
ALTER TABLE `projectdetail`
  MODIFY `runid` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `welddetail`
--
ALTER TABLE `welddetail`
  MODIFY `weld_id` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
