import unittest
from unittest.mock import patch, MagicMock

# Import the functions to test
# Ensure your ip_tool.py has: 
# if __name__ == "__main__": window.mainloop()
from ip_tool import get_ip_info, type_text_blue_details

class TestIPInformationTool(unittest.TestCase):

    @patch("ip_tool.requests.get")
    @patch("ip_tool.type_text_blue_details")
    def test_get_ip_info_success(self, mock_type_text, mock_requests_get):
        """
        Test get_ip_info with mocked network responses.
        Verifies that type_text_blue_details is called with correct data.
        """

        # Mock response for ipinfo.io
        mock_ipinfo_response = MagicMock()
        mock_ipinfo_response.status_code = 200
        mock_ipinfo_response.json.return_value = {
            "ip": "1.2.3.4",
            "ipv6": "abcd::1234",
            "hostname": "testhost",
            "city": "TestCity",
            "region": "TestRegion",
            "country": "TC",
            "loc": "0,0",
            "org": "TestOrg",
            "postal": "12345",
            "timezone": "UTC"
        }

        # Mock response for ipwhois.app
        mock_ipwhois_response = MagicMock()
        mock_ipwhois_response.status_code = 200
        mock_ipwhois_response.json.return_value = {
            "asn": "AS1234",
            "isp": "TestISP",
            "country_code": "TC"
        }

        # Configure requests.get to return these mocks in order
        mock_requests_get.side_effect = [mock_ipinfo_response, mock_ipwhois_response]

        # Call the function
        get_ip_info()

        # Ensure type_text_blue_details was called once
        mock_type_text.assert_called_once()

        # Check the content passed to type_text_blue_details
        output_text = mock_type_text.call_args[0][0]
        self.assertIn("IPv4 Address: 1.2.3.4", output_text)
        self.assertIn("ASN: AS1234", output_text)
        self.assertIn("ISP: TestISP", output_text)
        self.assertIn("Country Code: TC", output_text)

    @patch("ip_tool.requests.get")
    @patch("ip_tool.messagebox.showerror")
    def test_get_ip_info_failure(self, mock_showerror, mock_requests_get):
        """
        Test get_ip_info when network request fails.
        Verifies that an error message is shown.
        """
        # Configure requests.get to raise an exception
        mock_requests_get.side_effect = Exception("Network error")

        # Call the function
        get_ip_info()

        # Ensure messagebox.showerror was called with the exception message
        mock_showerror.assert_called_once()
        args, _ = mock_showerror.call_args
        self.assertIn("Network error", args[1])

if __name__ == "__main__":
    unittest.main()
