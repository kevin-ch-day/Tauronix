CREATE TABLE `company_info` (
  `CompanyID` int(11) NOT NULL,
  `CompanyName` varchar(255) NOT NULL,
  `Location` varchar(255) DEFAULT NULL,
  `StockSymbol` varchar(10) DEFAULT NULL,
  `note` varchar(200) DEFAULT NULL
);

CREATE TABLE `data_breach_disclosures` (
  `DisclosureID` int(11) NOT NULL,
  `CompanyID` int(11) NOT NULL,
  `DisclosureDate` date NOT NULL,
  `Perpetrators` varchar(200) DEFAULT NULL,
  `Description` text DEFAULT NULL,
  `Impact` text DEFAULT NULL
);

CREATE TABLE `dow_jones` (
  `Date` date NOT NULL,
  `Price` decimal(10,2) DEFAULT NULL,
  `Open` decimal(10,2) DEFAULT NULL,
  `High` decimal(10,2) DEFAULT NULL,
  `Low` decimal(10,2) DEFAULT NULL,
  `Volume` varchar(20) DEFAULT NULL,
  `Change_Percent` decimal(5,2) DEFAULT NULL
);

CREATE TABLE `stock_data` (
  `CompanyID` int(11) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Open` decimal(15,6) DEFAULT NULL,
  `High` decimal(15,6) DEFAULT NULL,
  `Low` decimal(15,6) DEFAULT NULL,
  `Close` decimal(15,6) DEFAULT NULL,
  `AdjClose` decimal(15,6) DEFAULT NULL,
  `Volume` int(11) DEFAULT NULL
);

CREATE TABLE `threat_actors` (
  `GangID` int(11) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Formation` year(4) DEFAULT NULL,
  `Founder` varchar(255) DEFAULT NULL,
  `Type` varchar(255) DEFAULT NULL,
  `Headquarters` varchar(255) DEFAULT NULL,
  `Region` varchar(255) DEFAULT NULL,
  `Methods` text DEFAULT NULL,
  `Membership` int(11) DEFAULT NULL,
  `members` text DEFAULT NULL,
  `OfficialLanguage` varchar(50) DEFAULT NULL,
  `Affiliations` varchar(255) DEFAULT NULL
);