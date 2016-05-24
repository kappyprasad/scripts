#drop view if exists `donkey`.`mule_logs`;

CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `donkey`.`mule_logs` AS
    SELECT 
		`m`.`id` as `id`,
        `m`.`when` as `when`,
        `s`.`name` AS `server`,
        `f`.`name` AS `file`,
        `l`.`name` AS `level`,
        `k`.`name` AS `key`,
        `m`.`description` AS `description`
    FROM
        (((((`donkey`.`message` `m`
        JOIN `donkey`.`file` `f`)
        JOIN `donkey`.`key` `k`)
        JOIN `donkey`.`level` `l`)
        JOIN `donkey`.`thread` `t`)
        JOIN `donkey`.`server` `s`)
    WHERE
        ((`m`.`file_id` = `f`.`id`)
            AND (`m`.`key_id` = `k`.`id`)
            AND (`m`.`level_id` = `l`.`id`)
            AND (`m`.`thread_id` = `t`.`id`)
            AND (`m`.`server_id` = `s`.`id`))