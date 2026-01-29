INSERT INTO model (id, name, trim, manufacturer_id, horsepower)
VALUES 
-- 	((SELECT distinct(name) FROM manufacturer where name = 'BMW') || '-3S', '3-Series', '4 Doors', 3, 200)
  ((SELECT distinct(name) FROM manufacturer where name = 'Toyota') || '-CO', 'Corolla', '2 Doors', 1, 170),
  ((SELECT distinct(name) FROM manufacturer where name = 'Tesla') || '-Y', 'Model Y', '4 Doors', 5, 180)

