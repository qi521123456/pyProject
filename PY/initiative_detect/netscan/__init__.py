try:
    from pymongo.errors import ServerSelectionTimeoutError
    from pymongo import MongoClient,collection
    from utils.xml_util import *
    from utils.mongodb import *
    from utils.mysql import *
    from utils.logging import *
    from docx.shared import Inches
    from docx import Document
    from docx.shared import Pt
    from bs4 import BeautifulSoup
    from functools import reduce
    import geoip2.database
    import requests
    import datetime
    import json
    import time
    import re
    import os
except Exception as ex:
    print(ex)