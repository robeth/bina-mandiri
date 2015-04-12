CREATE VIEW `transaction_pembelian_recap` AS
SELECT extract(YEAR FROM `transaction_pembelian_total`.`tanggal`) AS `year`,
       extract(MONTH FROM `transaction_pembelian_total`.`tanggal`) AS `month`,
       sum(`transaction_pembelian_total`.`total`) AS `total`
FROM `transaction_pembelian_total`
WHERE 1
GROUP BY extract(YEAR FROM `transaction_pembelian_total`.`tanggal`),
         extract(MONTH FROM `transaction_pembelian_total`.`tanggal`)
ORDER BY extract(YEAR FROM `transaction_pembelian_total`.`tanggal`) DESC,
	extract(MONTH FROM `transaction_pembelian_total`.`tanggal`) DESC