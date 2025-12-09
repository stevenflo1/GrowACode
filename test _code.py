import unittest
from unittest.mock import patch, MagicMock
from ip_tool import get_ip_info, type_text_blue_details

class TestIPInformationTool(unittest.TestCase):

    @patch("ip_tool.requests.get")
    @patch("ip_tool.type_text_blue_details")
    def test_get_ip_info_success(self, mock_type_text, mock_requests_get):
        # Mock IP info response
        mock_ipinfo = MagicMock(status_code=200)
        mock_ipinfo.json.return_value = {
            "ip": "1.2.3.4", "ipv6": "abcd::1234", "hostname": "host",
            "city": "City", "region": "Region", "country": "CC",
            "loc": "0,0", "org": "Org", "postal": "12345", "timezone": "UTC"
        }

        # Mock IPWhois response
        mock_ipwhois = MagicMock(status_code=200)
        mock_ipwhois.json.return_value = {"asn": "AS1234", "isp": "ISP", "country_code": "CC"}

        mock_requests_get.side_effect = [mock_ipinfo, mock_ipwhois]
        mock_widget = MagicMock()

        get_ip_info(widget=mock_widget)

        mock_type_text.assert_called_once()
        output_text = mock_type_text.call_args[0][0]
        self.assertIn("IPv4 Address: 1.2.3.4", output_text)
        self.assertIn("ASN: AS1234", output_text)

    @patch("ip_tool.requests.get")
    @patch("ip_tool.messagebox.showerror")
    def test_get_ip_info_failure(self, mock_showerror, mock_requests_get):
        mock_requests_get.side_effect = Exception("Network error")
        mock_widget = MagicMock()

        get_ip_info(widget=mock_widget)
        mock_showerror.assert_called_once()
        args, _ = mock_showerror.call_args
        self.assertIn("Network error", args[1])

if __name__ == "__main__":
    unittest.main()
