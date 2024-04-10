import cdsapi

c = cdsapi.Client()

start_year = 1900
end_year = 2020
year = start_year
while(year < end_year):
    for month in range(1,12):
        print('year: ', year, ', month: ', month)
        c.retrieve(
            'insitu-observations-surface-land',
            {
                'format': 'zip',
                'time_aggregation': 'monthy',
                'variable': [
                    'accumulated_precipitation', 'air_temperature', 'fresh_snow',
                    'snow_depth', 'snow_water_equivalent', 'wind_from_direction',
                    'wind_speed',
                ],
                'usage_restrictions': [
                    'restricted', 'unrestricted',
                ],
                'data_quality': [
                    'failed', 'passed',
                ],
                'year': f'{year}',
                'month': f'{month}',
                'day': [
                    '01', '02', '03',
                    '04', '05', '06',
                    '07', '08', '09',
                    '10', '11', '12',
                    '13', '14', '15',
                    '16', '17', '18',
                    '19', '20', '21',
                    '22', '23', '24',
                    '25', '26', '27',
                    '28', '29', '30',
                    '31',
                ],
            },
            f'{year}_{month}.zip')
    year += 1