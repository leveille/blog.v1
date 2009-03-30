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
        "Pylons>=0.9.7",
        "SQLAlchemy>=0.5,<=0.5.99",
        "Mako",
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'wurdig': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors={'wurdig': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = wurdig.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
