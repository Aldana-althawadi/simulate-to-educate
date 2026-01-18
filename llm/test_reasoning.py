from llm.llm_handler import analyze_email

email = """
Your Facebook account has been suspended.
Verify immediately to avoid permanent deletion:
http://fb-security-check[.]com
"""

print(analyze_email(email))
