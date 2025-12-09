import unittest
from unittest.mock import patch, MagicMock
import os
import tkinter as tk
from ip_tool import get_ip_info, type_text_blue_details  # adjust import to your file name

# Ensure headless environment
os.environ["DISPLAY"] = ":99"

class TestIPTool(unittest.TestCase):

    def setUp(self):
        # Create a hidden Tkinter root for headless tests
        self.root = tk.Tk()
        self.root.withdraw()
        self.text_widget = tk.Text(self.root)
        self.text_widget.pack()

    def tearDown(self):
        self.root.destroy()

    def test_type_text_blue_details_inserts_text(self):
        output = (
            "IP Address: 1.2.3.4\n"
            "Country: Wonderland\n"
            "Region: Magic\n"
            "City: RabbitHole\n"
            "Postal: 12345\n"
            "Timezone: UTC+1\n"
            "Country Code: WL\n"
        )
        type_text_blue_details(output, self.text_widget, delay=0)
        content = self.text_widget.get("1.0", tk.END)
        self.assertIn("IP Address: 1.2.3.4", content)
        self.assertIn("Country: Wonderland", content)

    @patch("ip_tool.requests.get")
    def test_get_ip_info_success(self, mock_get):
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

        # Patch the text widget in the module
        with patch("ip_tool.result_box", self.text_widget):
            get_ip_info()
            content = self.text_widget.get("1.0", tk.END)
            self.assertIn("IP Address: 1.2.3.4", content)

    @patch("ip_tool.requests.get")
    def test_get_ip_info_api_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": False, "message": "API error"}
        mock_get.return_value = mock_response

        with patch("ip_tool.messagebox.showerror") as mock_error:
            get_ip_info()
            mock_error.assert_called_with("Error", "API error")

    @patch("ip_tool.requests.get")
    def test_get_ip_info_exception(self, mock_get):
        mock_get.side_effect = Exception("Network failure")
        with patch("ip_tool.messagebox.showerror") as mock_error:
            get_ip_info()
            mock_error.assert_called_with("Error", "Network failure")


if __name__ == "__main__":
    unittest.main()
