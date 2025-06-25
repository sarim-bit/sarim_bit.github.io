/*

Data Validation

1. The data needs to have the 100 rows of Youtube channels. [Row count check]
2. The data must have four columns. [Column count check]
3. The channel name must be string, and the other columns must be integer. [Data type check]
4. Each row must have a unique channel name. [Distinct value check]

Row count: 100
Coulumn Count: 4

Data type
	channel_name: var_char
	subscriber_count: integer
	view_count: integer
	video_count: integer

Duplicate Count: 0
*/

-- Row count
SELECT 
	COUNT(*) AS num_row
FROM 
	view_uk_youtubers
-- PASSED

-- Column count
SELECT 
	COUNT(*) AS num_column
FROM 
	INFORMATION_SCHEMA.COLUMNS
WHERE 
	TABLE_NAME = 'view_uk_youtubers'
-- PASSED

-- Data Type Check
SELECT 
	COLUMN_NAME,
	DATA_TYPE
FROM 
	INFORMATION_SCHEMA.COLUMNS
WHERE 
	TABLE_NAME = 'view_uk_youtubers'
-- PASSED

-- Distinct Row Check
SELECT
	COUNT(DISTINCT(channel_name)) AS channel_count
FROM
	view_uk_youtubers

-- Alternate method
SELECT
	channel_name,
	COUNT(*) AS duplicate_count
FROM view_uk_youtubers
GROUP BY channel_name
HAVING COUNT(*) > 1

-- PASSED