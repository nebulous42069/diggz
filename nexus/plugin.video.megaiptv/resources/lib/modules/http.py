
import requests
from .utils import Log

def UrlValidator(url):
	ok=True
	try:
		r = requests.get(url,timeout=5)
		r.raise_for_status()
	except requests.exceptions.HTTPError as errh:
		Log(f"Http Error:{errh}")
		ok=False
	except requests.exceptions.ConnectionError as errc:
		Log(f"Error Connecting:{errc}")
		ok=False
	except requests.exceptions.Timeout as errt:
		Log(f"Timeout Error:{errt}")
		ok=False
	except requests.exceptions.RequestException as err:
		Log(f" Something Else:{err}")
		ok=False
	return ok