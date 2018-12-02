CREATE TABLE measurement (
    city_id         int not null,
    logdate         date not null,
    peaktemp        int,
    unitsales       int
) PARTITION BY RANGE (logdate);

CREATE TABLE measurement_y2006m02 PARTITION OF measurement
    FOR VALUES FROM ('2006-02-01') TO ('2006-03-01');

CREATE TABLE measurement_y2006m03 PARTITION OF measurement
    FOR VALUES FROM ('2006-03-01') TO ('2006-04-01');

CREATE INDEX ON measurement_y2006m02 (logdate);

CREATE TABLE reg2partitioned( city_id int not null, logdate date not null, peaktemp int, unitsales int);

CREATE TABLE partitioned2reg( city_id int not null, logdate date not null, peaktemp int, unitsales int ) PARTITION BY RANGE (logdate);
