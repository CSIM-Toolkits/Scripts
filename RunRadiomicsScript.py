import os
import sys
import optparse

arguments = sys.argv

# if len(sys.argv)!=4:
#     print "Wrong number of arguments. Usage: script.py InputImage InputMask BinWidth"
#
# INPUTIMAGE = arguments[1]
# INPUTMASK = arguments[2]
# try:
#     BINWIDTH = float(arguments[3])
# except:
#     print "Couldn't convert BinWidth to float. Check input parameters order and try again."
#     sys.exit()

required = "InputImage InputMask OutputTable".split()

parser = optparse.OptionParser("usage: %prog -i inputImage -m inputMask -b binWidth -o outputTable")
parser.add_option("-i", dest="InputImage", type='string', help="Input image path", metavar="INPUT IMAGE")
parser.add_option("-m", dest="InputMask", type='string', help="Input mask path", metavar="INPUT MASK")
parser.add_option("-b", dest="BinWidth", type='float', default=25.0, help="Bin width", metavar="BIN WIDTH")
parser.add_option("-o", dest="OutputTable", type='string', help="Output table prefix", metavar="OUTPUT TABLE PREFIX")

(options, args) = parser.parse_args()

for r in required:
    if options.__dict__[r] is None:
        parser.error("parameter %s required"%r)

InputImage = options.InputImage
InputMask = options.InputMask
BinWidth = options.BinWidth
OutputTable = options.OutputTable

#Gets Radiomics module
slicer.modules.slicerradiomics.createNewWidgetRepresentation()
widget = slicer.modules.SlicerRadiomicsWidget

#Reads image and mask
(success, inputImgNode)=slicer.util.loadVolume(InputImage, returnNode=True)
if not success:
    print "Couldn't read input image file. Check input parameters and try again."
    sys.exit()

(success, inputMskNode)=slicer.util.loadLabelVolume(InputMask, returnNode=True)
if not success:
    print "Couldn't read input mask file. Check input parameters and try again."
    sys.exit()

#Sets input volumes
widget.inputVolumeSelector.setCurrentNode(inputImgNode)
widget.inputMaskSelector.setCurrentNode(inputMskNode)

#Selects all features
widget.calculateAllFeaturesButton.click()

#Checks wavelet feature box
widget.waveletCheckBox.click()

#Sets Bin width
widget.binWidthSliderWidget.setValue(BinWidth)

#Creates output and adds it to scene
outputNode = slicer.vtkMRMLTableNode()
slicer.mrmlScene.AddNode(outputNode)

#Sets output node
widget.outputTableSelector.setCurrentNode(outputNode)

#Run module
widget.applyButton.click()

#Save file
txtfile=OutputTable + ".txt"
csvfile=OutputTable + ".csv"

print txtfile, csvfile
successtxt = slicer.util.saveNode(outputNode, txtfile)
successcsv = slicer.util.saveNode(outputNode, csvfile)

if not successcsv and not successtxt:
    print "Couldn't write table file. Check output prefix and try again."

exit(EXIT_SUCCESS)