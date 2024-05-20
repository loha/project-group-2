import re
import datetime

def is_only_chars(value: str):
  return bool(re.match(r"[A-z]+", value));

def is_phone(value: str):
  return bool(re.match(r"\+380[0-9]", value));

def is_uuid(uuid_string):
  pattern = r"[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}"  # UUID version 4 pattern
  return bool(re.match(pattern, uuid_string))

def is_date(value):
    match = re.search(r"^\d{4}\.\d{2}.\d{2}$", value)
    return bool(match)