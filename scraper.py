import pandas as pd
import json
import time
import requests
from requests.structures import CaseInsensitiveDict
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from datetime import datetime
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
def flatten_json(y):
	out = {}

	def flatten(x, name=''):
		if type(x) is dict:
			for a in x:
				flatten(x[a], name + a + '_')
		elif type(x) is list:
			i = 0
			for a in x:
				flatten(a, name + str(i) + '_')
				i += 1
		else:
			out[name[:-1]] = x

	flatten(y)
	return out
def get_profile(registration_no):

	url = "https://pmc.gov.pk/api/DRC/GetQualifications"

	headers = CaseInsensitiveDict()
	headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
	headers["Accept"] = "application/json, text/javascript, */*; q=0.01"
	headers["Accept-Language"] = "en-GB,en;q=0.5"
	headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
	headers["X-Requested-With"] = "XMLHttpRequest"
	headers["Origin"] = "https://pmc.gov.pk"
	headers["Connection"] = "keep-alive"
	# headers["Referer"] = "https://pmc.gov.pk/Doctors/Details?regNo=1520-N"
	headers["Sec-Fetch-Dest"] = "empty"
	headers["Sec-Fetch-Mode"] = "cors"
	headers["Sec-Fetch-Site"] = "same-origin"

	data = f"RegistrationNo={registration_no}"


	resp = requests.post(url, headers=headers, data=data,verify=False)
	if resp.status_code==200:
		data = json.loads(resp.text)['data']
		print(f"{registration_no}: Success")
		return data
	else:
		print(f"{registration_no}: Failed")
if __name__ == '__main__':
	print('Script Initialized.....\n\n')
	filepath = 'PMC.xlsx'
	main_df = pd.read_excel(filepath)
	registration_numbers= main_df['Registration No.'].tolist()
	dfs = []
	skips = []
	for registration_no in registration_numbers:
		try:
			data = get_profile(registration_no)
		except:
			skips.append(registration_no)

		df = flatten_json(data)
	#     df = pd.DataFrame.from_dict([data])
		dfs.append(df)
	df = pd.DataFrame(dfs)
	skips_df = pd.DataFrame({"reg_no":skips})
	current_datetime = datetime.now().strftime("%Y_%m_%d-%I_%M_%p")
	df.to_excel(f'output {current_datetime}.xlsx',index=False)
	skips_df.to_excel(f"skipped {current_datetime}.xlsx",index=False)
	input('\n\nScraping Finished!!!\nPress a key to exit.')