import unittest
from unittest.mock import patch, MagicMock

# Import your module
# from ip_tool import get_ip_info

class TestIPInformationTool(unittest.TestCase):

    @patch("requests.get")
    def test_get_ip_info_success(self, mock_get):
        # Mock response for ipinfo.io
        mock_response_ipinfo = MagicMock()
        mock_response_ipinfo.status_code = 200
        mock_response_ipinfo.json.return_value = {
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
        mock_response_ipwhois = MagicMock()
        mock_response_ipwhois.status_code = 200
        mock_response_ipwhois.json.return_value = {
            "asn": "AS1234",
            "isp": "TestISP",
            "country_code": "TC"
        }

        # Side effects for requests.get
        mock_get.side_effect = [mock_response_ipinfo, mock_response_ipwhois]

        # Patch type_text_blue_details to intercept call
        with patch("ip_tool.type_text_blue_details") as mock_type_text:
            from ip_tool import get_ip_info  # Import inside patch
            get_ip_info()

            # Ensure it was called once
            mock_type_text.assert_called_once()

            # Check the output contains expected text
            output_text = mock_type_text.call_args[0][0]
            self.assertIn("IPv4 Address: 1.2.3.4", output_text)
            self.assertIn("ASN: AS1234", output_text)
            self.assertIn("ISP: TestISP", output_text)
            self.assertIn("Country Code: TC", output_text)

if __name__ == "__main__":
    unittest.main()
