#!/usr/bin/env python

import unittest
import os
import subprocess
import shutil
import tempfile
import sys
import stat
import imp
import inspect

def checkPresent(myDict,myStream):
    for l in myStream:
        for k,v in  myDict.iteritems():
            repo=v['name'].split(':')[0]
            tag=v['name'].split(':')[1]
            if repo in l and tag in l :
                v['found']=True
    present=True
    for v in  myDict.itervalues():
        present &= v['found']
    return present

def printDockerImagesSad(hdr,myDict):
    cmd="docker images"
    p=subprocess.Popen(cmd.split(), stderr=sys.stderr, stdout=subprocess.PIPE,
                       shell=False)
    print("\n\nFAILURE--%s-- Images ->"%(hdr))
    for l in p.stdout:
        print ("%s",l)
    print ("Looking for:")
    for k,v in myDict.iteritems():
        print("%s found = %s"%(v['name'],v['found']))

class TestContainersBuilt(unittest.TestCase):
    def setUp(self):
        self.sdkTargets = os.environ['TARGETS'].split()
        self.sdkYPRelease = os.environ['YP_RELEASE']
        self.zephyrRelease = os.environ['ZEPHYR_RELEASE']
        self.ostroRelease =  os.environ['OSTRO_RELEASE']
        self.sdkCropsRelease = os.environ['CROPS_RELEASE']
        self.travisSlug = os.environ['TRAVIS_REPO_SLUG']
        self.dockerhubRepo = os.environ['DOCKERHUB_REPO']
        print("travisSlug=%s"%(self.travisSlug))
        print("dockerhubRepo=%s"%(self.dockerhubRepo))
        self.baseD={}
        self.baseD['i686']={}
        self.baseD['i686']['name']="%s/toolchain-base:%s"%(self.dockerhubRepo,"latest")
        self.baseD['i686']['found']=False

    def tearDown(self):
        pass


    def test_base_containers_built(self):
        cmd = """docker  images """
        p=subprocess.Popen(cmd.split(), stderr=sys.stderr, stdout=subprocess.PIPE,
                        shell=False)
        check=self.baseD
        allBuilt=checkPresent(check,p.stdout)
        if not allBuilt:
            # error information is more useful than true is not false
            printDockerImagesSad(inspect.stack()[0][3],check)

        self.assertTrue(allBuilt)



if __name__ == '__main__':
    unittest.main()
