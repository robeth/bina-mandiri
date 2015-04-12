CREATE VIEW `transaction_penjualan_recap` AS
SELECT extract(YEAR FROM `transaction_penjualan_total`.`tanggal`) AS `year`,
       extract(MONTH FROM `transaction_penjualan_total`.`tanggal`) AS `month`,
       sum(`transaction_penjualan_total`.`total`) AS `total`
FROM `transaction_penjualan_total`
GROUP BY extract(YEAR FROM `transaction_penjualan_total`.`tanggal`),
         extract(MONTH FROM `transaction_penjualan_total`.`tanggal`)
ORDER BY extract(YEAR FROM `transaction_penjualan_total`.`tanggal`) DESC,
	extract(MONTH FROM `transaction_penjualan_total`.`tanggal`) DESC