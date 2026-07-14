"""Unit tests for the golden-path weather service."""

from fastapi.testclient import TestClient

from main import app, forecast_for

client = TestClient(app)


class TestForecast:
    def test_is_deterministic(self):
        assert forecast_for("jakarta") == forecast_for("Jakarta ")

    def test_condition_is_known(self):
        assert forecast_for("bandung")["condition"] in {
            "sunny", "cloudy", "rainy", "windy", "stormy"
        }

    def test_temperature_in_range(self):
        temp = forecast_for("surabaya")["temperature_c"]
        assert 15 <= temp <= 34

    def test_blank_city_falls_back(self):
        assert forecast_for("   ")["city"] == "nowhere"


class TestRouter:
    def test_healthz_reports_ok(self):
        response = client.get("/healthz")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_weather_defaults_to_jakarta(self):
        response = client.get("/weather")
        assert response.status_code == 200
        assert response.json()["city"] == "jakarta"

    def test_weather_with_city(self):
        response = client.get("/weather?city=Bandung")
        assert response.status_code == 200
        assert response.json()["city"] == "bandung"

    def test_unknown_path_is_404(self):
        assert client.get("/does-not-exist").status_code == 404

    def test_wrong_method_on_known_path_is_405(self):
        assert client.post("/weather").status_code == 405
