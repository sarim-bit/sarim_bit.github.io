/*

Data Cleaning
1. Select only the required columns
3. Rename column names

*/

CREATE VIEW view_uk_youtubers AS

SELECT 
	channel_name,
	total_subscribers AS subscriber_count,
	total_views AS view_count,
	total_videos AS video_count 
FROM 
	top_uk_youtubers