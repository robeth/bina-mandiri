CREATE VIEW `transaction_pembelian_total` AS
SELECT `p`.`id` AS `id`,
       `p`.`tanggal` AS `tanggal`,
       sum((`s`.`jumlah` * `s`.`harga`)) AS `total`
FROM ((`transaction_pembelian` `p`
       JOIN `transaction_pembelian_stocks` `ps` on((`p`.`id` = `ps`.`pembelian_id`)))
      JOIN `transaction_stok` `s` on((`ps`.`stok_id` = `s`.`id`)))
GROUP BY `p`.`id`
ORDER BY `p`.`tanggal`