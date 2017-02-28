import fontTools.ttLib
import os
from ynlib.system import Execute


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
	def __init__(self, path):
		self.path = path
		self.TTFont = fontTools.ttLib.TTFont(self.path)

		self._glyphNames = []
		self._unicodes = []
		self._glyphClasses = []

		self._glyphs = {}
		for table in self.TTFont["cmap"].tables:
			for cmapEntry in table.cmap.items():
				self._addGlyph(cmapEntry[1], cmapEntry[0])

		self.postScriptName = str(self.TTFont['name'].getName(6, 1, 0, 0))

	def version(self):
		return str(self.TTFont['name'].getName(6, 1, 0, 0)).split(';')[0]

	def __repr__(self):
		return "<ftFont '%s'>" % (os.path.basename(self.path))

	def _addGlyph(self, name, _unicode):
		if not name in self._glyphNames:
			self._glyphs[name] = Glyph(self, name, _unicode)
#			self._glyphNames.append(name)

	def glyphs(self):
		# Return all glyphs as list
		return [self._glyphs[x] for x in self._glyphs.keys()]

	def glyphNames(self):
		return self.TTFont.getGlyphNames()

	def glyph(self, key):
		# Return single glyph
		if self._glyphs.has_key(key):
			return self._glyphs[key]
		# by Unicode
		else:
			for glyph in self.glyphs():
				if key == glyph.unicode:
					return glyph

	def unicodes(self):
		if not self._unicodes:
			for g in self.glyphs():
				if g.unicode:
					self._unicodes.append(g.unicode)
		return self._unicodes

	def features(self):
		_features = []
		for i, lookup in enumerate(self.TTFont['GSUB'].table.LookupList.Lookup):
			for featureRecord in self.TTFont['GSUB'].table.FeatureList.FeatureRecord:
				if not featureRecord.FeatureTag in _features and i in featureRecord.Feature.LookupListIndex:
					_features.append(featureRecord.FeatureTag)
					break
		return _features

	def lookupsPerFeature(self, featureName):
		_lookups = []
		for l, lookup in enumerate(self.TTFont['GSUB'].table.LookupList.Lookup):
			for featureRecord in self.TTFont['GSUB'].table.FeatureList.FeatureRecord:
				if l in featureRecord.Feature.LookupListIndex and featureRecord.FeatureTag == featureName:
					for i in range(lookup.SubTableCount):
						_lookups.append([featureRecord, lookup.SubTable[i]])
		return _lookups

	def stylisticSetName(self, feature):
		for r in self.TTFont['GSUB'].table.FeatureList.FeatureRecord:
			if r.FeatureTag == feature:
				return self.TTFont['name'].getName(r.Feature.FeatureParams.UINameID, 1, 0, 0)


	def defaultNumerals(self):
		n = ['.osf', '.tosf', '.lf', '.tf']
		for g in self.TTFont.getGlyphNames():
			if '.osf' in g and '.osf' in n:
				n.remove('.osf')
			if '.tosf' in g and '.tosf' in n:
				n.remove('.tosf')
			if '.lf' in g and '.lf' in n:
				n.remove('.lf')
			if '.tf' in g and '.tf' in n:
				n.remove('.tf')
		return n[0].replace('.', '')

	def numerals(self):
		has = []
		num = ['.osf', '.tosf', '.lf', '.tf']
		for g in self.TTFont.getGlyphNames():
			for n in num:
				if n in g and not n in has:
					has.append(n)
		return [x.replace('.', '') for x in has]

	def glyphClasses(self):
		if not self._glyphClasses:
			for g in self.TTFont.getGlyphNames():


				parts = g.split('.')
				for part in parts[1:]:
					if not part in self._glyphClasses:
						self._glyphClasses.append(part)
		return self._glyphClasses

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

	def scripts(self):
		_scripts = []
		for scriptRecord in self.TTFont['GSUB'].table.ScriptList.ScriptRecord:
			_scripts.append(scriptRecord.ScriptTag)
		return _scripts

	def languages(self):
		_languages = []
		for scriptRecord in self.TTFont['GSUB'].table.ScriptList.ScriptRecord:
			for langSys in scriptRecord.Script.LangSysRecord:
				lang = langSys.LangSysTag.strip()
				if not lang in _languages:
					_languages.append(lang)

		return _languages

	def lookupsPerFeatureScriptAndLanguage(self, featureName, scriptName = None, languageName = None):
		_features = []
		for scriptRecord in self.TTFont['GSUB'].table.ScriptList.ScriptRecord:
#			print vars(scriptRecord.Script)
			
			_features.extend(scriptRecord.Script.DefaultLangSys.FeatureIndex)

			if scriptName:

				for languageSystem in scriptRecord.Script.LangSysRecord:
					if scriptRecord.ScriptTag == scriptName:
						if languageSystem.LangSysTag.strip() == languageName:
							_features.extend(languageSystem.LangSys.FeatureIndex)
#			else:
				#	print languageSystem

#		print _features

		_subTables = []
		for i in _features:
			if self.TTFont['GSUB'].table.FeatureList.FeatureRecord[i].FeatureTag == featureName:
				featureTag = self.TTFont['GSUB'].table.FeatureList.FeatureRecord[i]
				for lookupIndex in featureTag.Feature.LookupListIndex:
					lookup = self.TTFont['GSUB'].table.LookupList.Lookup[lookupIndex]
					return lookup.SubTable

		return []

	def featureComparisonString(self, featureName):
#		string = ''
#		print featureName
#		for x in self.lookupsPerFeatureScriptAndLanguage(featureName):
#			print str(vars(x))
		return ''.join([str(vars(x)) for x in self.lookupsPerFeatureScriptAndLanguage(featureName)])

	def shrink(self, outputFilePath, freezeFeatures = [], removeFeatures = [], nameSuffix = None, glyphs = []):

		tempFile = outputFilePath.replace('.otf', '.temp.otf')

		pyftfeatfreeze = None
		pyftfeatfreezes = ['/home/juicie/wsgi/tools/pyftfeatfreeze.py', '/Users/yanone/Webseiten/wsgi/tools/pyftfeatfreeze.py']
		for f in pyftfeatfreezes:
			if os.path.exists(f):
				pyftfeatfreeze = f
				break

		pyftsubset = None
		pyftsubsets = ['/usr/local/bin/pyftsubset', '/home/juicie/wsgi/tools/pyftsubset.py', '/Users/yanone/Webseiten/wsgi/tools/pyftsubset.py']
		for f in pyftsubsets:
			if os.path.exists(f):
				pyftsubset = f
				break

		if pyftfeatfreeze and pyftsubset:

			replaceNaming = ""
			if nameSuffix:
				replaceNaming = "--replacenames '%s,%s'" % (self.postScriptName, self.postScriptName.replace('-', '%s-' % nameSuffix))

			# Feature freeze
#			call = "python '%s' %s --features '%s' %s --info '%s' '%s'" % (pyftfeatfreeze, replaceNaming, ','.join(freezeFeatures), ("--suffix --usesuffix '%s'" % nameSuffix) if nameSuffix else '', self.path, tempFile)
#			print call
#			Execute(call)

			# Subset
#			call = "python '%s' '%s' --name-languages='*' --name-legacy --name-IDs='*' --glyphs='*' --layout-features='tnum,ordn,pnum,subs,numr,lnum,dlig,sups,dnom,locl,ccmp,hist,ss18,zero,ss19,aalt,case,sinf,frac,liga'" % (pyftsubset, self.path)


			if glyphs:
				call = "python '%s' '%s' --name-languages='*' --name-legacy --name-IDs='*' --glyphs='%s' --layout-features='%s'" % (pyftsubset, self.path, ",".join(glyphs), ",".join(list(set(self.features()) - set(removeFeatures))))
#				call = "python '%s' '%s' --name-languages='*' --name-legacy --name-IDs='*' --glyphs='*' --layout-features='%s' --output-file='%s'" % (pyftsubset, tempFile, ",".join(list(set(self.features()) - set(['smcp', 'c2sc']))), outputFilePath)
#			call = "python '%s' '%s' --name-languages='*' --name-legacy --name-IDs='*' --glyphs='*' --layout-features='%s' --output-file='%s'" % (pyftsubset, tempFile, ",".join(list(set(self.features()) - (set(freezeFeatures) | set(removeFeatures)))), outputFilePath)
#			call = "python '%s' '%s' --verbose --name-languages='*' --name-legacy --name-IDs='*' --unicodes='*' --layout-features-='%s' --output-file='%s'" % (pyftsubset, tempFile, ",".join(list((set(freezeFeatures) | set(removeFeatures)))), outputFilePath)
			print call
			print Execute(call)



f = Font('/Users/yanone/Schriften/Font Produktion/Fonts/NonameSans-Regular.otf')

glyphs = []
for g in f.glyphNames():
	if not '.sc' in g:
		glyphs.append(g)

f.shrink('/Users/yanone/Schriften/Font Produktion/Fonts/NonameSansOffice-Regular.otf', glyphs = glyphs)
#f.shrink('/Users/yanone/Schriften/Font Produktion/Fonts/NonameSansOffice-Regular.otf', freezeFeatures = ['lnum', 'tnum', 'zero'], removeFeatures = ['smcp', 'c2sc', 'pnum'], nameSuffix = 'Office')

