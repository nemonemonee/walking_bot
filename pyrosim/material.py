from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

    def __init__(self, colorName, colorString):

        self.depth  = 3

        self.string1 = '<material name="'+colorName+'">'

        self.string2 = colorString

        self.string3 = '</material>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
