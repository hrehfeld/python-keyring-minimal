#!/usr/bin/env python3

import gi

gi.require_version('Secret', '1')


from gi.repository import Secret

SCHEMA_LABEL_KEY = 'Title'
SCHEMA_USERNAME_KEY = 'UserName'
SCHEMA_NOTES_KEY = 'Notes'
SCHEMA_URL_KEY = 'URL'


EXAMPLE_SCHEMA = Secret.Schema.new(
    "org.mock.type.Store",
    Secret.SchemaFlags.DONT_MATCH_NAME,
    {
        SCHEMA_USERNAME_KEY: Secret.SchemaAttributeType.STRING,
        SCHEMA_LABEL_KEY: Secret.SchemaAttributeType.STRING,
        SCHEMA_NOTES_KEY: Secret.SchemaAttributeType.STRING,
        SCHEMA_URL_KEY: Secret.SchemaAttributeType.STRING,
    }
)


def get_password(label, username=None):
    attrs = { SCHEMA_LABEL_KEY: label }
    if username is not None:
        attrs[SCHEMA_USERNAME_KEY] = username
        
    return Secret.password_lookup_sync(EXAMPLE_SCHEMA, attrs, None)


def set_password(label, password, username, notes=None, url=None):
    attributes = {}
    if username is not None:
        attributes[SCHEMA_USERNAME_KEY] = username
    if notes is not None:
        attributes[SCHEMA_NOTES_KEY] = notes
    if url is not None:
        attributes[SCHEMA_URL_KEY] = url

    Secret.password_store_sync(EXAMPLE_SCHEMA, attributes, Secret.COLLECTION_DEFAULT,
                               label, password, None)

def test(args):
    set_password('label', 'a password', 'a username')
    set_password('label with url', 'a password', 'a username', notes='here are some notes.', url='https://test.de')


    print(get_password('label'))
    print(get_password('label', 'a username'))
    print(get_password('label', 'another username'))


def get(args):
    pw = (get_password(args.label, args.username))
    if pw is None:
        exit(1)
    print(pw)


def set(args):
    set_password(args.label, args.password, args.username, args.notes, args.url)


def main():
    import argparse
    p = argparse.ArgumentParser()

    subp = p.add_subparsers(title='mode')

    testp = subp.add_parser('test')
    testp.set_defaults(func=test)

    getp = subp.add_parser('get')
    getp.set_defaults(func=get)
    getp.add_argument('label')
    getp.add_argument('--username')

    setp = subp.add_parser('set')
    setp.set_defaults(func=set)
    setp.add_argument('label')
    setp.add_argument('password')
    setp.add_argument('--username')
    setp.add_argument('--notes')
    setp.add_argument('--url')

    args = p.parse_args()

    args.func(args)
