CREATE VIEW `transaction_out_penjualan` AS
SELECT `sd`.`kode` AS `kode`,
       sum(`p`.`jumlah`) AS `jumlah`
FROM (`transaction_stok_det` `sd`
      JOIN `transaction_detailpenjualan` `p` on((`sd`.`id` = `p`.`stok_id`)))
GROUP BY `sd`.`kode`
ORDER BY `sd`.`kode`