from os import getenv
from setuptools import setup


with open("README.md", 'r') as f:
	long_description = f.read()


project_name = "sse-py"
git_url = "https://github.com/lwashington3/SSE.py"
github_token = getenv("GITHUB_TOKEN")


setup(
	name="sse-py",
	version="1.0.0",
	author="Len Washington III",
	description="Python Server Side Events Library",
	include_package_data=True,
	long_description=long_description,
	long_description_content_type="test/markdown",
	url=git_url,
	project_urls={
		"Bug Tracker": f"{git_url}/issues"
	},
	license="MIT",
	packages=[project_name],
	install_requires=[],
	classifiers=[
		"Programming Language :: Python :: 3.10"
	]
)
