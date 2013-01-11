#!/usr/bin/python

from bitbucket import bitbucket

authors = ['angelnan','albertnan','zikzakmedia','openlabs','cjbarnes18',
        'trytonspain','grasbauer','zodman','pokereichlich','ukoma',
        'ianjosephwilson','sharoonthomas','pokoli']

modules = {}
for author in authors:
    modules[author] ={}
    bb = bitbucket.Bitbucket(author)
#    print bb.get_repository('sale_kit')

#    exit(0)
    (resp,repos) = bb.public_repos()
    for repo in repos:
        if repo['language'] != 'python':
            continue
 #       if res:
 #           print bbrepo.get_branches()
        url="ssh://%s@bitbucket.org/%s/%s"%(repo[u'scm'], author,repo['name'])
        modules[author][repo['name']]={
            'module':repo['name'],
            'scm':repo['scm'],
            'url':url,
            'buildout':'%(name)s = %(scm)s %(url)s\n'%{
                'name': repo['name'],
                'scm': repo['scm'],
                'url': url,} 
        }


for author in modules:
    with open( author+".txt", 'w') as packages_file:
        for mod,val in modules[author].iteritems():
            packages_file.write(val['buildout'])
            print val['buildout']

#    print repos





