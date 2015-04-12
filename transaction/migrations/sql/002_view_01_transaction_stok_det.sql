CREATE VIEW `transaction_stok_det` AS
SELECT `s`.`id` AS `id`,
       `k`.`kode` AS `kode`,
       `k`.`nama` AS `nama`,
       `k`.`deskripsi` AS `deskripsi`,
       `s`.`tanggal` AS `tanggal`,
       `s`.`jumlah` AS `jumlah`,
       `s`.`harga` AS `harga`,
       `k`.`stabil` AS `stabil`,
       `k`.`fluktuatif` AS `fluktuatif`
FROM (`transaction_kategori` `k`
      JOIN `transaction_stok` `s` on((`k`.`id` = `s`.`kategori_id`)))