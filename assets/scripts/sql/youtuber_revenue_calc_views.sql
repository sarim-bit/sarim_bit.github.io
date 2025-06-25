/*

1. Define the variables
2. Create a CTE that calculates the average views per video
3. Select necessary columns
4. Filter the result to get the top three channels with most views

*/

-- Step 1
DECLARE @conversion_rate FLOAT = 0.02;		 -- Conversion rate is 2%
DECLARE @product_cost MONEY = 5.0;			 -- Product cost is £5
DECLARE @campaign_cost MONEY = 50000.0;		 -- Campaign cost is £50000


-- Step 2
WITH ChannelInfo AS (
	SELECT 
		channel_name,
		subscriber_count,
		view_count,
		video_count,
		ROUND((CAST(view_count AS FLOAT)/video_count), -4) AS rounded_avg_views_per_video
	FROM
		view_uk_youtubers

)

-- Top 3 channels with most views
SELECT TOP 3
	channel_name,
	rounded_avg_views_per_video,
	(rounded_avg_views_per_video * @conversion_rate) AS pot_products_sold_per_video,
	(rounded_avg_views_per_video * @product_cost) AS pot_revenue_per_video,
	(rounded_avg_views_per_video * @product_cost - @campaign_cost) AS net_profit
FROM 
	ChannelInfo
ORDER BY 
	view_count DESC

	