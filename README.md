# TT-Sprint_4_Project
The project for sprint 4

Summary of EDA: Main concern is missing values. 
	-- Price:       Will replace missing values with average for that model and year
	-- Odometer:    Will replace missing values with median for that model
	-- Model Year:  Can use the model to replace this, otherwise it will be missing
	-- paint color: irrelevant
	-- is 4wd:      irrelevant - is a flag field so first confirm any real nulls, if only one value, then fill with opposite value
	-- date fields: cannont replace

Featured visualizations during EDA:
	-- price distribution
	-- odometer distribution (type?)
	-- model year by manufacturer
	
	-- scatterplots:
	-- price vs Odometer
	-- price vs year
	-- odometer vs year
	