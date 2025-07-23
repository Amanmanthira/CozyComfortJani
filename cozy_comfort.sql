-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jul 23, 2025 at 09:30 PM
-- Server version: 8.0.18
-- PHP Version: 7.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cozy_comfort`
--

-- --------------------------------------------------------

--
-- Table structure for table `blankets`
--

DROP TABLE IF EXISTS `blankets`;
CREATE TABLE IF NOT EXISTS `blankets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `material` varchar(100) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `manufacturer_stock` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `blankets`
--

INSERT INTO `blankets` (`id`, `name`, `material`, `price`, `manufacturer_stock`) VALUES
(6, 'New Fleece Blanket', 'Polyester, Polyester Blend', '4500.00', 450),
(2, 'Sateen Stripe- Regular Size ', 'Cotton', '1850.00', 1000),
(3, 'Bare Home Fleece Blanket ', 'Microfiber', '2000.00', 300),
(4, 'Bare Home Comforter', '	Microfiber', '2400.00', 260),
(5, 'BEDELITE Fleece Blanket', 'Polyester, Polyester Blend', '4500.00', 450);

-- --------------------------------------------------------

--
-- Table structure for table `blanket_requests`
--

DROP TABLE IF EXISTS `blanket_requests`;
CREATE TABLE IF NOT EXISTS `blanket_requests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `distributor_id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `material` varchar(255) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `description` text,
  `image` varchar(255) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'pending',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `distributor_inventory`
--

DROP TABLE IF EXISTS `distributor_inventory`;
CREATE TABLE IF NOT EXISTS `distributor_inventory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `distributor_id` int(11) NOT NULL,
  `blanket_id` int(11) NOT NULL,
  `stock` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `distributor_id` (`distributor_id`),
  KEY `blanket_id` (`blanket_id`)
) ENGINE=MyISAM AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `distributor_inventory`
--

INSERT INTO `distributor_inventory` (`id`, `distributor_id`, `blanket_id`, `stock`) VALUES
(22, 3, 2, 100),
(23, 2, 2, 100),
(24, 2, 6, 12);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
CREATE TABLE IF NOT EXISTS `orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `seller_id` int(11) DEFAULT NULL,
  `distributor_id` int(11) DEFAULT NULL,
  `blanket_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `status` enum('pending','approved','shipped','delivered') DEFAULT 'pending',
  PRIMARY KEY (`id`),
  KEY `seller_id` (`seller_id`),
  KEY `distributor_id` (`distributor_id`),
  KEY `blanket_id` (`blanket_id`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `seller_id`, `distributor_id`, `blanket_id`, `quantity`, `status`) VALUES
(8, 3, 2, 2, 8, 'approved');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `role` enum('manufacturer','distributor','seller') NOT NULL,
  `distributor_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `fk_distributor` (`distributor_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`, `distributor_id`) VALUES
(1, 'manufacturer', 'manu123', 'manufacturer', NULL),
(2, 'distributor', 'dist123', 'distributor', NULL),
(3, 'seller', 'sell123', 'seller', 2);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
