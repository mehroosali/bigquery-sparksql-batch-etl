import pyspark 

from pyspark import SparkContext 
from pyspark.sql import SQLContext
from pyspark.conf import SparkConf
from pyspark.sql.session import SparkSession
from datetime import date 

spark = SQLContext(sc)

current_date = date.today()

file_name = str(current_date)

bucket_name = "gs://bucket_name"

flights_data = spark.read.json(bucket_name+"/flights-data/"+file_name+".json")

flights_data.registerTempTable("flights_data")

spark.sql("select max(distance) from flights_data limit 10").show()

qry = """
        select 
            flight_date , 
            round(avg(arrival_delay),2) as avg_arrival_delay,
            round(avg(departure_delay),2) as avg_departure_delay,
            flight_num 
        from 
            flights_data 
        group by 
            flight_num , 
            flight_date 
      """

avg_delays_by_flight_nums = spark.sql(qry)

query = """
        select 
            *,
            case 
                when distance between 0 and 500 then 1 
                when distance between 501 and 1000 then 2
                when distance between 1001 and 2000 then 3
                when distance between 2001 and 3000 then 4 
                when distance between 3001 and 4000 then 5 
                when distance between 4001 and 5000 then 6 
            END distance_category 
        from 
            flights_data 
        """

flights_data = spark.sql(query)

flights_data.registerTempTable("flights_data")

qry = """
        select 
            flight_date , 
            round(avg(arrival_delay),2) as avg_arrival_delay,
            round(avg(departure_delay),2) as avg_departure_delay,
            distance_category 
        from 
            flights_data 
        group by 
            distance_category , 
            flight_date 
      """

avg_delays_by_distance_category = spark.sql(qry)

output_flight_nums = bucket_name+"/flights_data_output/"+file_name+"_flight_nums"
output_distance_category = bucket_name+"/flights_data_output/"+file_name+"_distance_category"

avg_delays_by_flight_nums.coalesce(1).write.format("json").save(output_flight_nums)
avg_delays_by_distance_category.coalesce(1).write.format("json").save(output_distance_category)