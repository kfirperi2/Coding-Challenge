insert into vehicle (vin, model_id, fuel_id, model_year, purchase_price, description)
values
(
	'JTDBR32E123456789',
	(select id from model where name = 'Corolla'),
	(select id from fuel where type = 'Regular Gasoline'),
	2023,
	22800.00,
	'Sedan, white exterior, black seats'
)