import fontTools.ttLib
import os


class Glyph(object):
	def __init__(self, parent, name, _unicode = None):
		self.parent = parent
		self.name = name
		self.unicode = _unicode

		# To be set later
		self._bounds = None
		self.width = self.parent.TTFont.getGlyphSet()[self.name].width
	
	def __repr__(self):
		return "<ftGlyph '%s' %s>" % (self.name, self.unicode)

	def bounds(self):
		if not self._bounds:
			from fontTools.pens.boundsPen import BoundsPen, ControlBoundsPen
			pen = BoundsPen(None)
			self.parent.TTFont.getGlyphSet()[self.name].draw(pen)
			self._bounds = pen.bounds
		return self._bounds

class Font(object):
	def __init__(self, fontfilepath):
		self.fontfilepath = fontfilepath
		self.TTFont = fontTools.ttLib.TTFont(self.fontfilepath)

		self.glyphNames = []
		self._unicodes = []

		self._glyphs = {}
		for table in self.TTFont["cmap"].tables:
			for cmapEntry in table.cmap.items():
				self._addGlyph(cmapEntry[1], cmapEntry[0])

	def version(self):
		return str(self.TTFont['name'].getName(5, 1, 0, 0)).split(';')[0]

	def __repr__(self):
		return "<ftFont '%s'>" % (os.path.basename(self.fontfilepath))

	def _addGlyph(self, name, _unicode):
		if not name in self.glyphNames:
			self._glyphs[name] = Glyph(self, name, _unicode)
#			self.glyphNames.append(name)

	def glyphs(self):
		# Return all glyphs as list
		return [self._glyphs[x] for x in self._glyphs.keys()]

	def glyph(self, key):
		# Return single glyph
		return self._glyphs[key]

	def unicodes(self):
		if not self._unicodes:
			for g in self.glyphs():
				if g.unicode:
					self._unicodes.append(g.unicode)
		return self._unicodes

	def bounds(self):
		return self.boundsWithGlyphs(self.glyphs())

	def boundsByUnicodes(self, unicodes):
		_glyphs = []
		for glyph in self.glyphs():
			if glyph.unicode in unicodes:
				_glyphs.append(glyph)
		return self.boundsWithGlyphs(_glyphs)

	def boundsWithGlyphs(self, glyphs):
		left = None
		bottom = None
		right = None
		top = None

		for glyph in glyphs:
			bounds = glyph.bounds()
			if bounds:
				if not left:
					left = bounds[0]
				else:
					left = min(left, bounds[0])
				if not bottom:
					bottom = bounds[1]
				else:
					bottom = min(bottom, bounds[1])
				if not right:
					right = bounds[2]
				else:
					right = max(right, bounds[2])
				if not top:
					top = bounds[3]
				else:
					top = max(top, bounds[3])

		return left, bottom, right, top


 
