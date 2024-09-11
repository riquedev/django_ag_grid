import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_ag_grid",
    # version="0.0.1",
    use_scm_version=True,
    author="Henrique da Silva Santos",
    author_email="rique_dev@hotmail.com",
    description="A aG Grid Implementation for django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache License 2.0",
    url="https://github.com/riquedev/django_ag_grid",
    keywords="ag-grid, framework, django",
    project_urls={
        "Bug Tracker": "https://github.com/riquedev/django_ag_grid/issues",
        "Repository": "https://github.com/riquedev/django_ag_grid",
    },
    install_requires=[
        'Django>=3.2.14',
        'requests'
    ],
    classifiers=[
        "Framework :: Django",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ],
    packages=setuptools.find_packages(
        exclude=[
            'dj_ag_grid',
            'dj_ag_grid.*',
            'testapp',
            'testapp.*',
        ]),
    include_package_data=True,

    python_requires=">=3.7"
)
