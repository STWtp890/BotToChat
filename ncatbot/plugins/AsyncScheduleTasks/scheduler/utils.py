import re
from datetime import date
from datetime import datetime


async def slice_raw_msg(raw_msg: str) -> dict | None:
	"""
	- Transform raw message string to dict.
	- Param Example: "/ast -n task_name -t hello world -c cron_params -g true"
	- Return Example: {n: task_name,t: hello world,c: {cron_params},g: true}
	:param raw_msg: Original message string,
	:return: Variable 'msg_params' dict
	"""
	
	msg_params = {}
	origin_slice = re.split(r'-', raw_msg)
	for s in origin_slice:
		s.strip()
		s = s.split(r' ', 1)
		msg_params[s[0]] = s[1]
	msg_params['c'] = get_cron_params(msg_params['c'])
	msg_params['g'] = True if msg_params['g'] == 'true' else False
	msg_params['n'] = None if not msg_params['n'] else msg_params['n']
	msg_params['t'] = None if not msg_params['t'] else msg_params['t']
	return msg_params


async def get_cron_params(cron_str: str) -> dict | None:
	"""
	- Tansform cron expression string to dict.
	- Param Example: "re:year=2025 mon=5 day=1 hour=0 min=0 sec=0 week=? dowek=? start=? end=?"
	- Return Example: {year: 2025,mon: 5,day: 1,hour: 0,min: 0,sec: 0,wek: ?,dowek: ?,start: ?,end: ?}
	:param cron_str: Original cron expression string,
	:return: Variable 'cron_dicr' dict or None.
	"""
	
	if cron_str.find("re:", 0, 3):
		year = re.search(r'\byear=([\d/*\-,]+)?', cron_str).group(1) if cron_str.find("year") else '*'
		mon = re.search(r'\bmon=([\d/*\-,]+)?', cron_str).group(1) if cron_str.find("mon") else '*'
		day = re.search(r'\bday=([\d/*\-,]+)?', cron_str).group(1) if cron_str.find("day") else '*'
		hour = re.search(r'\bhour=([\d/*\-,]+)?', cron_str).group(1) if cron_str.find("hour") else '*'
		min = re.search(r'\bmin=([\d/*\-,]+)?', cron_str).group(1) if cron_str.find("min") else '*'
		sec = re.search(r'\bsec=([\d/*\-,]+)?', cron_str).group(1) if cron_str.find("sec") else '*'
		wek = re.search(r'\bwek=([\d/*\-,]+)?', cron_str).group(1) if cron_str.find("wek") else None
		dowek = re.search(r'\bdowek=([[\d/*\-,]+])?', cron_str).group(1) if cron_str.find("dowek") else None
		start = datetime.strptime(cron_str, "%Y/%m/%d %H:%M") if cron_str.find("start") else '*'
		end = datetime.strptime(cron_str, "%Y/%m/%d %H:%M") if cron_str.find("end") else '*'
		
		cron_dict = {
			'year': year,
			'month': mon,
			'day': day,
			'hour': hour,
			'minute': min,
			'second': sec,
			'week': wek,
			'day_of_week': dowek,
			'start_date': start,
			'end_date': end,
		}
		
		return cron_dict
	else:
		return None


if __name__ == '__main__':
	print(date(2023, 10, 1))
	print(datetime(2023, 10, 1, 0, 0, 0))
	
	datetime.strptime("2021-10-01", "%Y-%m-%d")
