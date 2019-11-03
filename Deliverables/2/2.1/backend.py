import json
import functools

class Backend:

	def sort(self, lst):
		if len(lst) != 10:
			raise Exception("input list not 10 objs long")
		if not self._list_valid(lst):
			raise Exception("input contains invalid special json")
		return self._sort(lst)
	
	def _list_valid(self, lst):
		for obj in lst:
			if not self._is_special_json(obj):
				return False
		return True

	def _is_special_json(self, obj):
		return isinstance(obj, (int, float, str)) or \
				(isinstance(obj, dict) and \
				"name" in obj and self._is_special_json(obj["name"]))

	def _sort(self, lst):
		lst.sort(key = functools.cmp_to_key(self._cmp))
		return lst

	def _cmp(self, x, y):
		## check to see if x and y are numeric
		if isinstance(x, (int, float)) and isinstance(y, (int, float)):
			return self._cmp_alphanumeric(x, y)

		## check to see if x and y are strings
		if isinstance(x, (str)) and isinstance(y, (str)):
			return self._cmp_alphanumeric(x, y)

		## check to see if x and y are both objects
		if isinstance(x, dict) and isinstance(y, dict):
			return self._cmp_objects(x, y)
		
		## else the objects mismatch
		return self._cmp_mismatch(x, y)

	def _cmp_alphanumeric(self, x, y):
		if x > y:
			return 1
		elif x < y:
			return -1
		return 0
	
	def _cmp_objects(self, x, y):
		return self._cmp(x['name'], y['name'])

	def _cmp_mismatch(self, x, y):
		if isinstance(x, (dict, str)) and isinstance(y, (int, float)):
			return 1
		if isinstance(x, dict) and isinstance(y, str):
			return 1
		return -1