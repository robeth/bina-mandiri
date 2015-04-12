CREATE VIEW `transaction_penjualan_total` AS
SELECT `p`.`id` AS `id`,
       `p`.`tanggal` AS `tanggal`,
       sum((`dp`.`jumlah` * `dp`.`harga`)) AS `total`
FROM (`transaction_penjualan` `p`
      JOIN `transaction_detailpenjualan` `dp` on((`p`.`id` = `dp`.`penjualan_id`)))
GROUP BY `p`.`id`