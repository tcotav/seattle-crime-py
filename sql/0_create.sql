CREATE DATABASE crime;

CREATE TABLE seattle_crime (
   event_clearance_code int,
   cad_event_number bigint,
   event_clearance_subgroup varchar(40),
   event_clearance_group  varchar(40),
   cad_cdw_id int unique primary key,
   event_clearance_date  datetime,
   zone_beat varchar(8),
   initial_type_description varchar(100),
   district_sector varchar(4),
   initial_type_subgroup varchar(40),
   hundred_block_location varchar(40),
   general_offense_number int,
   event_clearance_description varchar(40),
   longitude varchar(100),
   latitude varchar(100),
   initial_type_group varchar(40),
   census_tract varchar(40)
);
