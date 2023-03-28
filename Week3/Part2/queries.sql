
-- grouping sets

SELECT country, category, SUM(amount) AS totalsales
FROM FACTSALES AS fs 
LEFT JOIN DIMCOUNTRY AS dcount ON fs.countryid = dcount.countryid
LEFT JOIN DIMCATEGORY AS dcat ON fs.categoryid = dcat.categoryid
GROUP BY
	GROUPING SETS(country, category);



-- rollup

SELECT year, country, SUM(amount) AS totalsales
FROM FACTSALES AS fs 
LEFT JOIN DIMDATE AS dd ON fs.dateid = dd.dateid
LEFT JOIN DIMCOUNTRY AS dcount ON fs.countryid = dcount.countryid
GROUP BY
	GROUPING SETS(year, country)
ORDER BY year, country;


-- cube

SELECT year, country, AVG(amount) AS averagesales
FROM FACTSALES AS fs 
LEFT JOIN DIMDATE AS dd ON fs.dateid = dd.dateid
LEFT JOIN DIMCOUNTRY AS dcount ON fs.countryid = dcount.countryid
GROUP BY
	CUBE(year, country)
ORDER BY year, country;


-- creating mqt on ibm db2

CREATE TABLE total_sales_per_country (country, total_sales)AS(
SELECT country, SUM(amount) as total_sales_amount
FROM FACTSALES AS fs 
LEFT JOIN DIMCOUNTRY AS dcount ON fs.countryid = dcount.countryid
GROUP BY country)
WITH DATA;