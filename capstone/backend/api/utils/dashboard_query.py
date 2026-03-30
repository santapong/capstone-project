OVERALL_CHAT = """
SELECT 
    COUNT(*) as total_chat
FROM 
    logs
"""



TIME_USAGE = """
SELECT
	AVG(time_usage) as average_time_usage
FROM
	logs
"""



TOP_USER_TIME = """
WITH rename_recast as(

SELECT
	id
	,llm_model
	,prompt
	,question
	,answer
	,time_usage
	,CAST(datetime AS DATE) as date
from
	logs
),
count_usage as(

SELECT
	COUNT(*) as usage
	,date
from
	rename_recast
group by
	date
order by
    usage DESC
)

select * from count_usage
"""

PEAK_USER="""



"""

TOP_CATEGORY="""
SELECT 
	count(category) as count_category
	,category
from 
	category
group by 
	category
order by
	count_category DESC
"""

DOCUMENT_TABLE="""
SELECT * FROM documents

"""

HISTORY_TABLE="""
SELECT * FROM logs
"""

ERROR_PERCENTAGE="""
WITH count_error as(
Select
	count(answer) as answer
	-- Count Error
	,count(
	CASE
	WHEN LOWER(answer) like 'er%' THEN 1
	END
	) as error
from
	logs
), final as(
Select
	ROUND((answer - error) / answer::numeric, 4)*100 as diff
	,error
	,answer
from
	count_error
)

select * from final
"""

UPLOAD_PAGE="""
WITH SUM_TABLE as(
SELECT
	SUM(pages) as pages
	,ROUND(SUM(time_usage)::numeric, 2) as times
FROM documents
), FINAL as(
SELECT
	ROUND((times/pages)::numeric, 2) as time_usage_per_page
FROM
	SUM_TABLE
)

SELECT * FROM FINAL
"""