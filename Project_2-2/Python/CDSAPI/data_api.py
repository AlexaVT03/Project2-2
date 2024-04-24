import cdsapi

def fetch_data(year : list, coordinates : list) -> None:

    c = cdsapi.Client()
    
    for y in year:

        c.retrieve(
            'reanalysis-era5-single-levels',
            {
                'product_type': 'reanalysis',
                'format': 'grib',
                'variable': [
                    '10m_u_component_of_wind', '10m_v_component_of_wind', '2m_dewpoint_temperature',
                    '2m_temperature', 'evaporation', 'large_scale_precipitation',
                    'mean_total_precipitation_rate', 'precipitation_type', 'surface_pressure',
                    'total_cloud_cover', 'total_precipitation',
                ],
                'year': str(y),
                'month': [
                    '01', '02', '03',
                    '04', '05', '06',
                    '07', '08', '09',
                    '10', '11', '12',
                ],
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
                'time': [
                    '00:00', '06:00', '12:00',
                    '18:00',
                ],
                'area': coordinates,
            },
            f'{y}_data.grib')

# example for the Netherlands (let run for a while, large amount of data here)
fetch_data(
           year = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
           coordinates = [53.5, 3.5, 50.5, 7,]
          )