import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from ip_tool import get_ip_info, type_text_blue_details  # your main code

class TestIPTool(unittest.TestCase):

    def setUp(self):
        # Create a headless Tkinter root
        self.root = tk.Tk()
        self.root.withdraw()  # hide window in headless
        self.text_widget = tk.Text(self.root)
        self.text_widget.pack()

    def tearDown(self):
        self.root.destroy()

    @patch("ip_tool.requests.get")
    def test_type_text_blue_details_inserts_text(self, mock_get):
        # Prepare output text
        output = (
            "IP Address: 1.2.3.4\n"
            "Country: Wonderland\n"
            "Region: Magic\n"
            "City: RabbitHole\n"
            "Postal: 12345\n"
            "Timezone: UTC+1\n"
            "Country Code: WL\n"
        )
        # Call typing function with delay=0 for fast tests
        type_text_blue_details(output, self.text_widget, delay=0)

        # Check text widget content
        content = self.text_widget.get("1.0", tk.END)
        self.assertIn("IP Address: 1.2.3.4", content)
        self.assertIn("Country: Wonderland", content)

    @patch("ip_tool.requests.get")
    def test_get_ip_info_success(self, mock_get):
        # Mock successful API response
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

        # Patch the Text widget for insertion
        with patch("ip_tool.result_box", self.text_widget):
            get_ip_info()
            content = self.text_widget.get("1.0", tk.END)
            self.assertIn("IP Address: 1.2.3.4", content)

    @patch("ip_tool.requests.get")
    def test_get_ip_info_api_failure(self, mock_get):
        # Mock API failure
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": False, "message": "API error"}
        mock_get.return_value = mock_response

        with patch("ip_tool.messagebox.showerror") as mock_error:
            get_ip_info()
            mock_error.assert_called_with("Error", "API error")

    @patch("ip_tool.requests.get")
    def test_get_ip_info_exception(self, mock_get):
        # Simulate network error
        mock_get.side_effect = Exception("Network failure")
        with patch("ip_tool.messagebox.showerror") as mock_error:
            get_ip_info()
            mock_error.assert_called_with("Error", "Network failure")


if __name__ == "__main__":
    unittest.main()
