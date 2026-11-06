from unittest.mock import MagicMock, patch

# Mock BigQuery before importing main, so tests don't require GCP credentials.
with patch("google.cloud.bigquery.Client") as mock_client_class:
    mock_client_class.return_value = MagicMock()
    import main


@patch("main.client.get_table")
@patch("main.client.load_table_from_uri")
def test_main_success(mock_load_table, mock_get_table):
    mock_job = MagicMock()
    mock_load_table.return_value = mock_job

    mock_table = MagicMock()
    mock_table.num_rows = 50
    mock_get_table.return_value = mock_table

    with main.app.test_client() as test_client:
        response = test_client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "CSV loaded successfully",
        "table": "mlops-dev-513820.test_schema.us_states",
        "rows": 50,
    }

    mock_load_table.assert_called_once()
    mock_job.result.assert_called_once()
    mock_get_table.assert_called_once_with(
        "mlops-dev-513820.test_schema.us_states"
    )


@patch("main.client.get_table")
@patch("main.client.load_table_from_uri")
def test_main_empty_table(mock_load_table, mock_get_table):
    mock_job = MagicMock()
    mock_load_table.return_value = mock_job

    mock_table = MagicMock()
    mock_table.num_rows = 0
    mock_get_table.return_value = mock_table

    with main.app.test_client() as test_client:
        response = test_client.get("/")

    assert response.status_code == 200
    assert response.get_json()["rows"] == 0
    mock_job.result.assert_called_once()


@patch("main.client.load_table_from_uri")
def test_main_bigquery_load_failure(mock_load_table):
    mock_load_table.side_effect = RuntimeError("BigQuery load failed")

    with main.app.test_client() as test_client:
        response = test_client.get("/")

    assert response.status_code == 500 
    
