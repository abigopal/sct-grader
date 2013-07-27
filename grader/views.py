# Create your views here.

import os
import glob

from models import *

def createTestCases(prob, dir):
    counter = 1
    root = os.path.dirname(os.path.realpath(__file__))
    upload_path = os.path.join(root, dir)
    
    infiles = sorted(glob.glob(os.path.join(upload_path, '*.in')))
    outfiles = sorted(glob.glob(os.path.join(upload_path, '*.out')))
    print infiles
    print upload_path

    inputs = []
    outputs = []

    for filename in infiles:
        with open(filename, 'r') as input_file:
            inputs.append(input_file.read())

    for filename in outfiles:
        with open(filename, 'r') as output_file:
            outputs.append(output_file.read())

    if len(inputs) != len(outputs):
        raise 'Check upload'

    for i in range(len(inputs)):
        tc = TestCase(inp=inputs[i], out=outputs[i], num=(i+1), prob=prob)
        tc.save()

def createProblem(name, points, evaluator, lang):
    prob = Problem(name=name, points=points, evaluator=evaluator, lang=lang)
    prob.save()

createProblem('str', 10, 'txt', 'java')
