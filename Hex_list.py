from __future__ import division
import sublime, sublime_plugin, math, re

class HexListCommand(sublime_plugin.TextCommand):
	def split_n(self,string,n):
		result = []
		while(len(string)!=0):
			result.append(int(string[:n],16))
			string = string[n:]
		return result;
	def rgb_to_hsl(self,rgb):
		hue = 0;
		saturation = 0;
		var_rgb = []
		for i in rgb:
			var_rgb.append(round(i/255,2));
		c_min = min(var_rgb);
		c_max = max(var_rgb);
		c_delta = c_max - c_min
		lumin = math.ceil(((c_min+c_max)/2)*100);
		if(c_delta == 0):
			hue = 0;
			saturation = 0;
		else:
			if(c_max == var_rgb[0]):
				hue = 60*(((var_rgb[1]-var_rgb[2])/c_delta)%6)
			elif(c_max == var_rgb[1]):
				hue = 60*(((var_rgb[2]-var_rgb[0])/c_delta)+2)
			elif(c_max == var_rgb[2]):
				hue = 60*(((var_rgb[0]-var_rgb[1])/c_delta)+4)
			hue = round(hue,1);
			saturation = round(((c_delta/(1-math.fabs((2*lumin/100)-1)))*100));
		return int(hue),int(saturation),int(lumin);
	def run(self, edit):
		view = self.view;
		for sels in view.sel():
			selection = view.substr(sels);
			selection = selection.replace("#","");
			match = re.match("^[a-fA-F0-9]*$",selection) is not None;
			if((len(selection) is 6) & (match)):
				rgb = self.split_n(selection,2);
				h,s,l = self.rgb_to_hsl(rgb);
				sublime.status_message("[HEX : #"+selection+"]  [RGB : "+str(rgb[0])+" "+str(rgb[1])+" "+str(rgb[2])+"]  [HSL : "+str(h)+" "+str(s)+" "+str(l)+"]");
			else:
				sublime.status_message("Error : Not a valid hex string");