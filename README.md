# Data-Driven Influencer Selection for YouTube Marketing Campaigns 


# Table of contents 

- [Objective](#objective)
- [Data Source](#data-source)
- [Stages](#stages)
- [Design](#design)
  - [Dashboard components](#dashboard-components)
  - [Tools](#tools)
- [Development](#development)
  - [End-to-End Approach](#end-to-end-approach)
  - [Data Exploration](#data-exploration)
  - [Data Cleaning](#data-cleaning)
  - [Transform the Data](#transform-the-data)
  - [Create the SQL View](#create-the-sql-view)
- [Data Validation](#data-validation)
- [Visualization](#visualization)
  - [Dashboard](#dashboard)
  - [DAX Measures](#dax-measures)
- [Analysis](#analysis)
  - [Findings](#findings)
  - [Profitability Prediction](#profitability-prediction)
  - [Summary](#summary)
- [Recommendations](#recommendations)
  - [Potential ROI](#potential-roi)
  - [Action Plan](#action-plan)



# Objective 

**The Key Question** 

Which UK-based YouTubers are the top performers, and who are the most suitable candidates for partnership in upcoming marketing campaigns?
The Head of Marketing is looking to identify the top-performing YouTubers to determine the most suitable partners for marketing campaigns planned for the remainder of the year.

**The Ideal Solution**

A dynamic, insight-driven dashboard that profiles leading UK YouTubers based on key metrics—subscriber count, total views, video output, and engagement rate. 
This dashboard will empower the marketing team to make informed, data-backed decisions when selecting YouTubers for collaboration, ensuring optimal reach and audience alignment.

# Data Source 

To support the analysis, we require data on the top UK-based YouTubers, specifically including the following attributes:
- Channel names
- Total subscribers
- Total views
- Total videos uploaded

The dataset is sourced from Kaggle. It includes information on the top 100 social media influencers by country for 2024. [Kaggle](https://www.kaggle.com/datasets/bhavyadhingra00020/top-100-social-media-influencers-2024-countrywise?resource=download)

## Getting latest data

To get the latest YouTuber statistics, use YouTube's API. The YouTube API requires the channel ID.

### Steps

1. Extract channel id from the Kaggle dataset. 
2. Create Python script, [uk_youtubers_latest_stats.py](assets/scripts/python/uk_youtubers_latest_stats.py), to get the relevant data from the API.

Code Snippet to get Channel data
```python
def get_channel_stats(youtube, channel_id):
    request = youtube.channels().list(
        part='snippet,statistics',
        id=channel_id
    )
    response = request.execute()
    if 'items' in response and response['items']:
        data = dict(
            channel_name=response['items'][0]['snippet']['title'],
            total_subscribers=response['items'][0]['statistics']['subscriberCount'],
            total_views=response['items'][0]['statistics']['viewCount'],
            total_videos=response['items'][0]['statistics']['videoCount'],
        )
        return data
    else:
        print("No 'items' found in response. Possibly invalid channel ID or restricted key.")
        return None
```
3. Store all the information in a new csv file [top_uk_youtubers.csv](assets/data/top_uk_youtubers.csv).

# Stages

- Design
- Development
- Data Validation
- Analysis 
 

# Design 

## Dashboard components
To determine the dashboard's content, we first identify the key business questions it needs to answer. These questions guide the design and ensure the dashboard delivers relevant and actionable insights.
1. Who are the top 10 YouTubers by subscriber count?
2. Which 3 channels have the highest total views?
3. Which 3 channels have the highest average views per video?
4. Which 3 channels have the highest views per subscriber ratio?
5. Which 3 channels have the highest subscriber engagement per video uploaded?
   

## Tools 

| Tool | Purpose |
| --- | --- |
| Excel | Exploring the data |
| SQL Server | Cleaning, testing, and analysing the data |
| Power BI | Visualising the data via interactive dashboards |
| GitHub | Hosting the project documentation and version control |


# Development

## End-to-End Approach

1. Data Collection

	Acquire relevant YouTube channel data, focusing on UK-based creators and key performance metrics.

3. Initial Exploration

	Conduct a preliminary review and analysis of the raw data in Excel to identify structure, completeness, and potential anomalies.

4. Data Loading

	Import the dataset into SQL Server to enable structured querying and efficient data handling.

5. Data Cleaning

	Use SQL to clean and transform the data, handling missing values, correcting inconsistencies, and preparing it for analysis.

6. Data Testing

	Validate data accuracy and consistency through SQL-based testing and integrity checks.

7. Data Visualisation

	Connect SQL Server to Power BI to build an interactive dashboard showcasing metrics like subscriber count, total views, video volume, and engagement.

8. Insight Generation

	Analyse trends and relationships within the visualised data to derive actionable insights for marketing decision-making.

9. Documentation & Commentary

	Document the process, methods, and key findings, including explanations for insights and any assumptions made.

10. Publishing

	Publish the final dashboard and supporting documentation to GitHub Pages for easy access and sharing.


## Data Exploration

A preliminary review of the dataset revealed the following key points:

1. Sufficient Core Metrics

	The dataset includes at least four essential columns: subscriber count, total views, number of videos, and engagement-related data. These cover all core metrics required for our analysis, meaning no further data collection from the client is necessary at this stage.

2. Channel Identification Format

	The first column appears to contain YouTube channel identifiers in a format that includes the @ symbol, likely representing channel handles. For clarity and usability, we’ll extract and clean these to display proper channel names throughout the analysis.

3. Language Inconsistencies

	Some column headers and cell values are in a language other than English. We'll assess whether these fields are relevant. If they are, translation or standardisation will be required; otherwise, they’ll be excluded from the analysis.

4. Unnecessary Columns

	The dataset contains more fields than needed for our specific objectives. To improve clarity and focus, non-essential columns will be removed during the data cleaning process, allowing us to streamline both analysis and visualisation.


## Data Cleaning 
The goal of the cleaning phase is to ensure the dataset is structured, consistent, and fully ready for analysis. To achieve this, the cleaned dataset should meet the following criteria and constraints:
1. Relevant Fields Only

	Retain only the columns essential to the analysis, such as channel name, subscriber count, total views, video count, and engagement metrics.

2. Correct Data Types

	Ensure that each column has an appropriate data type (e.g., integers for numerical metrics, strings for text fields) to support accurate filtering, aggregation, and visualisation.

3. No Missing Values

	All rows should contain complete data across the retained columns. There should be no null or blank values to ensure the reliability of any derived insights.


Below is a table outlining the constraints on our cleaned dataset:

| Property | Value |
| --- | --- |
| Number of Rows | 100 |
| Number of Columns | 4 |

And here is a tabular representation of the expected schema for the clean data:

| Column Name | Data Type | Nullable |
| --- | --- | --- |
| channel_name | VARCHAR | NO |
| total_subscribers | INTEGER | NO |
| total_views | INTEGER | NO |
| total_videos | INTEGER | NO |

### Transform the data 
```sql
/*

Data Cleaning
1. Select only the required columns
3. Rename column names

*/

SELECT 
	channel_name,
	total_subscribers AS subscriber_count,
	total_views AS view_count,
	total_videos AS video_count 
FROM 
	top_uk_youtubers
```


### Create the SQL view 

```sql
CREATE VIEW view_uk_youtubers AS

SELECT 
	channel_name,
	total_subscribers AS subscriber_count,
	total_views AS view_count,
	total_videos AS video_count 
FROM 
	top_uk_youtubers

```


# Data Validation 
The following data quality checks were conducted

## 1. Row count check
```sql
SELECT 
	COUNT(*) AS num_row
FROM 
	view_uk_youtubers
```
### Output
![Row Count](assets/images/row_count.png)

## 2. Column count check 
```sql
SELECT 
	COUNT(*) AS num_column
FROM 
	INFORMATION_SCHEMA.COLUMNS
WHERE 
	TABLE_NAME = 'view_uk_youtubers'
```
### Output
![Column Count](assets/images/column_count.png)


## 3. Data type check
```sql
SELECT 
	COLUMN_NAME,
	DATA_TYPE
FROM 
	INFORMATION_SCHEMA.COLUMNS
WHERE 
	TABLE_NAME = 'view_uk_youtubers'
```
### Output
![Data Type](assets/images/data_type_check.png)


## 4. Duplicate count check 
```sql
SELECT
	COUNT(DISTINCT(channel_name)) AS channel_count
FROM
	view_uk_youtubers
```
### Output
![Duplicate check](assets/images/distinct_row_check.png)

# Visualization 
## Dashboard

![GIF of Power BI Dashboard](assets/images/Dashboard.gif)

## DAX Measures

### 1. Total Subscribers
```
Total Subscribers (Million) =
DIVIDE(
  SUM(view_uk_youtubers[subscriber_count]),
  1000000
)
```

### 2. Total Views
```
Total Views (Billion) =
DIVIDE(
  SUM(view_uk_youtubers[view_count]),
  1000000000
)
```

### 3. Average Views Per Video
```
Average Views per Video (Million) = 
DIVIDE(
	SUM('view_uk_youtubers'[view_count]),
	SUM('view_uk_youtubers'[video_count]) * 1000000
)

```

### 4. Subscriber Engagement Rate
```
Subscriber Engagement = 
DIVIDE(
	SUM('view_uk_youtubers'[subscriber_count]),
	SUM('view_uk_youtubers'[video_count])
)

```

### 5. Views per subscriber
```
Views per Subscriber = 
DIVIDE(
	SUM('view_uk_youtubers'[view_count]),
	SUM('view_uk_youtubers'[subscriber_count])
)

```

# Analysis 

## Findings

To provide targeted insights for our marketing client, we will concentrate on answering the following key questions:


### 1. Who are the top 10 YouTubers with the most subscribers?

| Rank | Channel Name         | Subscribers (Million) |
|------|----------------------|-----------------|
| 1    | NoCopyrightSounds    | 34.10           |
| 2    | DanTDM               | 29.20           |
| 3    | Dan Rhodes           | 26.70           |
| 4    | Miss Katy            | 25.40           |
| 5    | KSI Music            | 25.00           |
| 6    | Mister Max           | 25.00           |
| 7    | Dua Lipa             | 24.30           |
| 8    | Jelly                | 23.50           |
| 9    | Sidemen              | 22.40           |
| 10   | Mrwhosetheboss       | 21.10           |



### 2. Which 3 channels have the most views?


| Rank | Channel Name | Total Views (Billion) |
|------|--------------|-----------------|
| 1    | Disney Kids  | 22.08           |
| 2    | DanTDM   	  | 20.20           |
| 3    | Dan Rhodes   | 19.20           |


### 3. Which 3 channels have the highest average views per video?

| Rank | Channel Name | Average Views per Video (Million) |
|------|--------------|-----------------|
| 1    | Mark Ronson  | 353.89          |
| 2    | Dua Lipa     | 46.77           |
| 3    | Jessie J     | 34.38           |


### 4. Which 3 channels have the highest views per subscriber ratio?

| Rank | Channel Name       | Views per Subscriber        |
|------|-----------------   |---------------------------- |
| 1    | Disney Kids        | 1623.74                     |
| 2    | Disney Club UK     | 1053.68                     |
| 3    | Woody & Kleiny     | 979.81                      |



### 5. Which 3 channels have the highest subscriber engagement rate per video uploaded?

| Rank | Channel Name    | Subscriber Engagement Rate  |
|------|-----------------|---------------------------- |
| 1    | Mark Ronson     | 355,500                     |
| 2    | Dua Lipa        | 77,388.54                   |
| 3    | Jessie J        | 60,335.20                   |




## Profitability Prediction  

### 1. Youtubers with the most subscribers 

#### Calculation breakdown

**Campaign idea -  Product Placement**
- Product cost is assumed to be £5
- Campaign cost is assumed to be £50,000
- Conversion rate is assumed to be 2%
  
1. NoCopyrightSounds 
- Average views per video = 6 million
- Product cost = £5
- Potential units sold per video = 6 million x 2% conversion rate = 120,000 units sold
- Potential revenue per video = 120,000 x £5 = £600,000
- Campaign cost (one-time fee) = £50,000
- **Net profit = £600,000 - £50,000 = £550,000**

b. DanTDM

- Average views per video = 5.36 million
- Product cost = £5
- Potential units sold per video = 5.36 million x 2% conversion rate = 107,200 units sold
- Potential revenue per video = 107,200 x £5 = £536,000
- Campaign cost (one-time fee) = £50,000
- **Net profit = £536,000 - £50,000 = £486,000**

c. Dan Rhodes

- Average views per video = 11.35 million
- Product cost = £5
- Potential units sold per video = 11.35 million x 2% conversion rate = 227,000 units sold
- Potential revenue per video = 227,000 x £5 = £1,135,000
- Campaign cost (one-time fee) = £50,000
- **Net profit = £1,135,000 - £50,000 = £1,085,000**


Best option from category: Dan Rhodes


#### SQL query 

```sql
/*

1. Define the variables
2. Create a CTE that calculates the average views per video
3. Select the necessary columns
4. Filter the result to get the top three most subscribed channels

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

-- Top 3 most subscribed channels
SELECT TOP 3
	channel_name,
	rounded_avg_views_per_video,
	(rounded_avg_views_per_video * @conversion_rate) AS pot_products_sold_per_video,
	(rounded_avg_views_per_video * @conversion_rate * @product_cost) AS pot_revenue_per_video,
	(rounded_avg_views_per_video * @conversion_rate * @product_cost - @campaign_cost) AS net_profit
FROM 
	ChannelInfo
ORDER BY 
	subscriber_count DESC;
```

#### Output

![Most subsc](assets/images/most_subscribed_youtubers.png)


### 2.  Youtubers with the most views 

#### Calculation breakdown

**Campaign idea - Influencer marketing**
- Campaign cost is assumed to be £130,000
- Conversion rate is assumed to be 2%

a. Disney Kids

- Average views per video = 4.6 million
- Product cost = £5
- Potential units sold per video = 4.6 million x 2% conversion rate = 92,000 units sold
- Potential revenue per video = 92,000 x £5 = £460,000
- Campaign cost (3-month contract) = £130,000
- **Net profit = £460,000 - £130,000 = £330,000**

b. DanTDM

- Average views per video = 5.36 million
- Product cost = £5
- Potential units sold per video = 5.36 million x 2% conversion rate = 107,200 units sold
- Potential revenue per video = 107,200 x £5 = £536,000
- Campaign cost (3-month contract) = £130,000
- **Net profit = £536,000 - £130,000 = £406,000**

c. Dan Rhodes

- Average views per video = 11.35 million
- Product cost = £5
- Potential units sold per video = 11.35 million x 2% conversion rate = 227,000 units sold
- Potential revenue per video = 227,000 x £5 = £1,135,000
- Campaign cost (3-month contract) = £130,000
- **Net profit = £1,135,000 - £130,000 = £1,085,000**


Best option from category: Dan Rhodes



#### SQL query 
```sql
/*

1. Define the variables
2. Create a CTE that calculates the average views per video
3. Select the necessary columns
4. Filter the result to get the top three channels with the most views

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

-- Top 3 channels with the most views
SELECT TOP 3
	channel_name,
	rounded_avg_views_per_video,
	(rounded_avg_views_per_video * @conversion_rate) AS pot_products_sold_per_video,
	(rounded_avg_views_per_video * @conversion_rate * @product_cost) AS pot_revenue_per_video,
	(rounded_avg_views_per_video * @conversion_rate * @product_cost - @campaign_cost) AS net_profit
FROM 
	ChannelInfo
ORDER BY 
	view_count DESC	
```

#### Output

![Most views](assets/images/most_viewed_youtubers.png)



## Summary

1. Top UK YouTubers by Subscribers

	NoCopyrightSounds, Dan Rhodes, and DanTDM lead the UK in subscriber count.

2. Top UK YouTubers by Views

	Disney Kids, DanTDM, and Dan Rhodes Max have the highest total views.

3. Channel Type Insights

	Entertainment and music-focused channels dominate engagement and reach. These creators publish consistently and maintain high levels of audience interaction, making them ideal for broad marketing campaigns.



## Recommendations 

1. Dan Rhodes is the strongest candidate for collaboration if the goal is to maximise visibility. He currently has the highest subscriber count among UK YouTubers.

2. For longer-term impact, DanTDM and Dan Rhodes are great partners due to their large subscriber bases and strong average view counts.

3. Based on consistent engagement and overall performance, the top three channels to partner with are:
- NoCopyrightSounds
- DanTDM
- Dan Rhodes

4. Disney Kids can be used for the promotion of any kids-specific products.

### Potential ROI 
1. Dan Rhodes collaboration: Estimated net profit: £1,085,000 per video

2. DanTDM
- Product placement campaign: £486,000 per video
- Influencer partnership deal: £406,000 net profit (one-off)

3. NoCopyrightSounds collaboration: Estimated profit: £550,000 per video 


### Action plan
We recommend pursuing a long-term influencer partnership with Dan Rhodes, given his extensive reach, consistent engagement, and high ROI potential.

After confirming this strategy aligns with the client’s expectations, we can look to expand collaborations with DanTDM and NoCopyrightSounds based on campaign results and performance tracking.   

1. Initiate Contact

	Reach out to Dan Rhodes’ team first to explore partnership opportunities.

2. Negotiate Terms

	Align collaboration agreements with campaign budgets and expected deliverables.

3. Launch Campaigns

	Begin with the agreed influencer content, tracking performance through defined KPIs.

4. Review and Optimise

	Evaluate each campaign’s performance, collect feedback from target audiences, and refine the strategy for future partnerships.
