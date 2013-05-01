#!/usr/bin/env python3

import cgi
import cgitb

# enable debugging
cgitb.enable()

page = """
<!DOCTYPE html>

<html>
<body>
<form action="searchTwitter.py" method="post">
<h1>Twitter Search</h1>
<p>
Enter a Search Query:
<input type="text" name="query">
</p>
<p>
<input type="submit" value="Search">
</p>
</form>
</body>
</html>
"""

print("Content-Type: text/html")
print()

print(page)
