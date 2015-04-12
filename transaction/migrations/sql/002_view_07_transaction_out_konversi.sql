CREATE VIEW `transaction_out_konversi` AS
SELECT `sd`.`kode` AS `kode`,
       sum(`d`.`jumlah`) AS `jumlah`
FROM (`transaction_stok_det` `sd`
      JOIN `transaction_detailin` `d` on((`sd`.`id` = `d`.`stok_id`)))
GROUP BY `sd`.`kode`
ORDER BY `sd`.`kode`