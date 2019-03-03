-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema vacays
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema vacays
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `vacays` DEFAULT CHARACTER SET utf8 ;
USE `vacays` ;

-- -----------------------------------------------------
-- Table `vacays`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vacays`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `full_name` VARCHAR(250) NULL,
  `username` VARCHAR(250) NULL,
  `password` VARCHAR(250) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `vacays`.`travel_plan`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vacays`.`travel_plan` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `destination` VARCHAR(250) NULL,
  `start_date` VARCHAR(250) NULL,
  `end_date` VARCHAR(250) NULL,
  `plan` VARCHAR(250) NULL,
  `created_at` DATETIME NULL,
  `updated_on` DATETIME NULL,
  `users_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_travel_plan_users_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_travel_plan_users`
    FOREIGN KEY (`users_id`)
    REFERENCES `vacays`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `vacays`.`users_travelplan`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vacays`.`users_travelplan` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `created_at` VARCHAR(250) NULL,
  `updated_at` VARCHAR(250) NULL,
  `users_id` INT NOT NULL,
  `travel_plan_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_users_travelplan_users1_idx` (`users_id` ASC) VISIBLE,
  INDEX `fk_users_travelplan_travel_plan1_idx` (`travel_plan_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_travelplan_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `vacays`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_travelplan_travel_plan1`
    FOREIGN KEY (`travel_plan_id`)
    REFERENCES `vacays`.`travel_plan` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
