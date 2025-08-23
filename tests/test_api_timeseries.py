class TestTimeSeriesAPI:
    def test_get_timeseries(self, testapp) -> None:
        response = testapp.get("/api/v1/timeseries", status=200)
        data = response.json
        assert isinstance(data, list)
        assert all(set(item.keys()) >= {"datetime", "value"} for item in data)
        assert any(isinstance(item["value"], float) for item in data)
    
    def test_valid_date_filter_format(self, testapp) -> None:
        response = testapp.get("/api/v1/timeseries?start_date=2025-08-19T22:34:13&end_date=2025-08-23T03:34:13", status=200)
        data = response.json
        assert isinstance(data,list)
        assert all(set(item.keys()) >= {"datetime", "value"} for item in data)
        assert any(isinstance(item["value"], float) for item in data)
    
    def test_valid_date_filter_format_out_of_bound(self, testapp) -> None:
        response = testapp.get("/api/v1/timeseries?start_date=2100-08-19T22:34:13&end_date=2100-08-23T03:34:13", status=200)
        data = response.json
        assert data == []

    def test_invalid_date_filter_format(self, testapp) -> None:
        response = testapp.get("/api/v1/timeseries?start_date=2024-12-3x", status=400)
        assert response.status_code == 400

    def test_invalid_request(self, testapp) -> None:
        response = testapp.get("/api/v1/timeseries_not_exist", status=404)
        assert response.status_code == 404

