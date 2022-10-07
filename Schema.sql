CREATE TABLE cleaned_combined_data (
  "country" TEXT PRIMARY KEY,
	"beer_servings" FLOAT,
	"spirit_servings" FLOAT,
	"wine_servings" FLOAT,
	"total_litres_of_pure_alcohol" FLOAT,
	"unemployment_rate" FLOAT
 	
);
	
	
select * from cleaned_combined_data 