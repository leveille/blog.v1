try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='Wurdig',
    version='0.1',
    description='A Simple Pylons Blog',
    author='Jason R. Leveille',
    author_email='leveillej@gmail.com',
    url='http://jasonleveille.com',
    install_requires=[
        "Pylons>=0.9.7,<=0.9.7.99",
        "SQLAlchemy>=0.5,<=0.5.99",
        "Beaker>=1.3.1,<=1.3.99",
        "Mako>=0.2.2,<=0.2.99",
        "AuthKit>=0.4.3,<=0.4.99",
        # requires tidy to be installed
        # http://countergram.com/software/pytidylib/docs/index.html#installing-tidylib
        "pytidylib>=0.1.1,<=0.1.99",
        "html5lib>=0.10,<=0.19",
        "cssutils>=0.9.6a0", 
        "Babel>=0.9.4,<=0.9.9",
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'wurdig': ['i18n/*/LC_MESSAGES/*.mo']},
    message_extractors={'wurdig': [
            ('**.py', 'python', None),
            ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
            ('templates/**.html', 'mako', {'input_encoding': 'utf-8'}),
            # ('public/**', 'ignore', None),
            ('public/javascripts/utils.js', 'javascript', {'input_encoding': 'utf-8'}),
            ('public/javascripts/application.js', 'javascript', {'input_encoding': 'utf-8'}),
            ('public/admin/js/admin.js', 'javascript', {'input_encoding': 'utf-8'})]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = wurdig.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
