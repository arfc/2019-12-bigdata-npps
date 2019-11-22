"""
Created on November 04, 2019
@author: mturkmen
comments: Interface for Serpent Simulation 
"""

from __future__ import division, print_function, unicode_literals, absolute_import
import warnings
warnings.simplefilter('default',DeprecationWarning)

import os
import copy
import sys

from GenericCodeInterface import GenericParser
from CodeInterfaceBaseClass import CodeInterfaceBase

sys.path.append("/projects/sciteam/bahg/projects/raven/framework/CodeInterfaces/Serpent/")
import SerpentParser

class Serpent(CodeInterfaceBase):

  def __init__(self):

    CodeInterfaceBase.__init__(self)
    self.inputExtensions  = []  
    self.outputExtensions = []    
    self.execPrefix       = ''     
    self.execPostfix      = ''      
    self.caseName         = None    
     
  def generateCommand(self,inputFiles,executable,clargs=None, fargs=None, preExec=None):

    if clargs==None:
      raise IOError('No input file was specified in clargs!')

    inFiles=inputFiles[:]
    extsClargs = list(ext[0][0] for ext in clargs['input'].values() if len(ext) != 0)
    extsFargs  = list(ext[0] for ext in fargs['input'].values())
    usedExts = extsClargs + extsFargs
    if len(usedExts) != len(set(usedExts)):
      raise IOError('GenericCodeInterface cannot handle multiple input files with the same extension.  You may need to write your own interface.')
    for inf in inputFiles:
      ext = '.' + inf.getExt() if inf.getExt() is not None else ''
      try:
        usedExts.remove(ext)
      except ValueError:
        pass
    if len(usedExts) != 0:
      raise IOError('Input extension',','.join(usedExts),'listed in XML node Code, but not found in the list of Input of <Files>')

    def getFileWithExtension(fileList,ext):

      found = False
      for index,inputFile in enumerate(fileList):
        if inputFile.getExt() == ext:
          found=True
          break
      if not found:
        raise IOError('No InputFile with extension '+ext+' found!')
      return index,inputFile

    todo = ''
    todo += clargs['pre']+' '
    todo += executable
    index=None
    #inputs
    for flag,elems in clargs['input'].items():
      if flag == 'noarg':
        for elem in elems:
          ext, delimiter = elem[0], elem[1]
          idx,fname = getFileWithExtension(inputFiles,ext.strip('.'))
          todo += delimiter + fname.getFilename()
          if index == None:
            index = idx
        continue
      todo += ' '+flag
      for elem in elems:
        ext, delimiter = elem[0], elem[1]
        idx,fname = getFileWithExtension(inputFiles,ext.strip('.'))
        todo += delimiter + fname.getFilename()
        if index == None:
          index = idx

    self.caseName = inputFiles[index].getBase()
    outFile = self.caseName+'.output'
    if 'output' in clargs:
      todo+=' '+clargs['output']+' '+outFile
    todo+=' '+clargs['text']

    todo+=' '+clargs['post']
    returnCommand = [('parallel',todo)],outFile
    print('Execution Command: '+str(returnCommand[0]))
    return returnCommand
    
  def createNewInput(self, currentInputFiles, origInputFiles, samplerType, **Kwargs):

    indexes=[]
    infiles=[]
    origfiles=[]
    #FIXME possible danger here from reading binary files
    for index,inputFile in enumerate(currentInputFiles):
      if inputFile.getExt() in self.getInputExtension():
        indexes.append(index)
        infiles.append(inputFile)
    for index,inputFile in enumerate(origInputFiles):
      if inputFile.getExt() in self.getInputExtension():
        origfiles.append(inputFile)
    parser = GenericParser.GenericParser(infiles)
    parser.modifyInternalDictionary(**Kwargs)
    parser.writeNewInput(infiles,origfiles)
    return currentInputFiles

  # def checkForOutputFailure(self,output,workingDir):

    # errorWord = "Input error:"
    # failure = True
    # try:
      # outputToRead = open(os.path.join(workingDir,output),"r")
    # except IOError:
    # # the output does not exist 
      # return failure    
    # readLines = outputToRead.readlines()
    # for goodMsg in errorWord:
      # if any(goodMsg in x for x in readLines):
        # failure = False
        # break
    # return failure

  def finalizeCodeOutput(self, command, output, workingDir):
    
    filename = command.strip().split(' ')[-1]
    res_file = os.path.join(workingDir,filename+"_res.m")
    det_file = os.path.join(workingDir,filename+"_det0.m")
    # below are the difference between original values and ref values
    #feedback_doppler_ref = (k_inf_ref - k_inf_ref_600) / 300
    #k_inf = float(SerpentParser.SearchKinf(res_file)) - k_inf_ref
    #conversion_ratio = float(SerpentParser.SearchConversionRatio(res_file)) - conversion_ratio_ref
    #fast_flux_graph = float(SerpentParser.SearchFastFluxGraph(det_file)) - fast_flux_graph_ref
    #feedback_doppler = (float(SerpentParser.SearchFeedbackDoppler(res_file)) - k_inf_ref_600) / 300 - feedback_doppler_ref
    # below for original values
 
    k_inf = SerpentParser.SearchKinf(res_file)
    conversion_ratio = SerpentParser.SearchConversionRatio(res_file)
    fast_flux_graph = SerpentParser.SearchFastFluxGraph(det_file)
    feedback_doppler = SerpentParser.SearchFeedbackDoppler(res_file)

    csv_filepath = os.path.join(workingDir, output+'.csv')
    SerpentParser.MakeCSV(csv_filepath, k_inf, conversion_ratio, fast_flux_graph,feedback_doppler)
