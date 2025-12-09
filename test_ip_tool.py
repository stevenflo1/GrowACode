import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from ip_tool import get_ip_info, type_text_blue_details  # assume your main code is saved as ip_tool.py

class TestIPTool(unittest.TestCase):

    def setUp(self):
        # Create a dummy Tkinter Text widget
        self.root = tk.Tk()
        self.text_widget = tk.Text(self.root)
        self.text_widget.pack()

    def tearDown(self):
        self.root.destroy()

    @patch("ip_tool.requests.get")
    def test_get_ip_info_success(self, mock_get):
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "ip": "1.2.3.4",
            "country": "Wonderland",
            "country_code": "WL",
            "region": "Magic",
            "city": "RabbitHole",
            "postal": "12345",
            "timezone": "UTC+1",
            "success": True
        }
        mock_get.return_value = mock_response

        # Patch the text widget to capture insert calls
        with patch.object(self.text_widget, "insert") as mock_insert:
            # call function with mocked widget
            output = (
                f"IP Address: 1.2.3.4\n"
                f"Country: Wonderland\n"
                f"Region: Magic\n"
                f"City: RabbitHole\n"
                f"Postal: 12345\n"
                f"Timezone: UTC+1\n"
                f"Country Code: WL\n"
            )
            type_text_blue_details(output, self.text_widget, delay=0)

            # Ensure insert was called at least once
            mock_insert.assert_called()

    @patch("ip_tool.requests.get")
    def test_get_ip_info_api_failure(self, mock_get):
        # Mock API response failure
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": False, "message": "API error"}
        mock_get.return_value = mock_response

        with patch("ip_tool.messagebox.showerror") as mock_error:
            get_ip_info()
            mock_error.assert_called_with("Error", "API error")

    @patch("ip_tool.requests.get")
    def test_get_ip_info_exception(self, mock_get):
        # Simulate a network error
        mock_get.side_effect = Exception("Network failure")
        with patch("ip_tool.messagebox.showerror") as mock_error:
            get_ip_info()
            mock_error.assert_called_with("Error", "Network failure")


if __name__ == "__main__":
    unittest.main()
