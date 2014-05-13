import sublime, sublime_plugin, locale, datetime
import calendar,locale

# view.run_command("dr_calendar_insert_month")

def add_month(y,m,x):
        r_m = m + x
        r_y = y
        if (r_m < 1):
            r_y -= 1
            r_m = 12
        if (r_m > 12):
            r_m = 1
            r_y += 1
        return (r_y,r_m)

class TDrCalend():
    def __init__(self,y,m):
        self.y = y
        self.m = m
        self.mc = self.GetMonthCalendarAsText()

    def GetMonthCalendarAsText(self):
        c = calendar.TextCalendar()
        mc = c.monthdatescalendar(self.y, self.m)
        today = datetime.date.today()#+datetime.timedelta(days=10) #debug
        self.dd = datetime.date(self.y, self.m, 1)
        # s = '{:      %B %Y}\n'.format(self.dd)
        s = '{0: %B %Y}'.format(self.dd)
        s = '{0: ^21}'.format(s)+"\n"
        # s += '\n'
        
        for w in mc:
            for d in w:
            	s += ' ' + '{0:%a}'.format(d)[0:2]
            s += '\n'
            break
        
        for w in mc:
            for d in w:
                if (d.month == self.m):
                    if d == today:
                        s += '{0:>3}'.format('*'+str(d.day))
                    else:
                        s += '{0:>3}'.format(d.day)
                else:
                    s += "   "
            s += "\n"
        return (s)


class DrMonthsCalendarOpen(sublime_plugin.TextCommand):
	def is_visible(self):
		return True
	def is_enabled(self):
		return True		
	def run(self, edit):	
		loc = locale.getlocale() # get current locale
		locale.setlocale(locale.LC_ALL, '')
		c = calendar.TextCalendar()
		# self.view.insert(edit, self.view.sel().begin(), c.formatmonth(2013,9))
		today = datetime.date.today()#+datetime.timedelta(days=10) #debug
		(pr_y, pr_m) = add_month(today.year,today.month,-1)
		c1 = TDrCalend(pr_y,pr_m).GetMonthCalendarAsText()
		c11 = c1.splitlines()
		c2 = TDrCalend(today.year,today.month).GetMonthCalendarAsText()
		c22 = c2.splitlines()
		(n_y, n_m) = add_month(today.year,today.month,1)
		c3 = TDrCalend(n_y,n_m).GetMonthCalendarAsText()
		c33 = c3.splitlines()
		c4 = []

		for x in range(0,8):
			if len(c11) <= x: 
				c4.append('{0: >23}'.format(""))
			else:
				c4.append('{0: >23}'.format(c11[x]))   # use '*' as a fill char
			if len(c22) <= x: 
				c4[x] = c4[x] + '  ' +'{0: <21}'.format("")
			else:
				c4[x] = c4[x] + '  ' +'{0: <21}'.format(c22[x])
			if len(c33) <= x:  
				c4[x] = c4[x] + '  ' +'{0: <21}'.format("")
			else:
				c4[x] = c4[x] + '  ' +'{0: <21}'.format(c33[x])

		# for pos in self.view.sel():
		# 	b = pos.begin()
		# 	rr = self.view.insert(edit, pos.begin(), "\n".join(c4)+'\n')			
		# 	r = sublime.Region(b, b+rr)
		# 	print ("\n".join(c4)+'\n')
		# 	self.view.add_regions('DrCalendar',[r],"keyword",'',sublime.HIDDEN)
			
		self.output_view = self.view.window().get_output_panel("textarea_drcalendar")
		self.view.window().run_command("show_panel", {"panel": "output.textarea_drcalendar"})
		# self.output_view.run_command("set_file_type", {"Packages/DrCalendar/DrCalendar.tmLanguage"})
		self.output_view.set_syntax_file("Packages/DrMonthsCalendar/DrCalendar.tmLanguage")
		self.output_view.set_read_only(False)

		# self.output_view.insert(edit, self.output_view.size(), today.strftime('   %A %x')+"\n\n")
		self.output_view.insert(edit, self.output_view.size(),"\n".join(c4))
		self.output_view.insert(edit, self.output_view.size(), "\n"+today.strftime('   %A %x'))
		

		
		# self.output_view.insert(edit, self.output_view.size(),"\n".join(c22)+'\n')
		
		# self.output_view.run_command("append", {"characters": "Hello, World!"})
		# self.output_view.set_read_only(True)
		# r = sublime.Region(1, 100)
		# # DRAW_OUTLINED
		# self.output_view.add_regions('DrCalendar',[r],"keyword",'',sublime.HIDDEN)
		# self.view.window().focusView(self.output_view)
		
		# self.view.window().show_quick_panel("123", None, sublime.MONOSPACE_FONT)


  		

class DrCalendarInsertMonthCommand1(sublime_plugin.TextCommand):
	def run(self, edit):
		loc = locale.getlocale() # get current locale
		locale.setlocale(locale.LC_ALL, '')
		c = calendar.TextCalendar()
		# self.view.insert(edit, self.view.sel().begin(), c.formatmonth(2013,9))
		i = len(self.view.sel())
		if i > 1 :
			i = -1
		for pos in self.view.sel():
			self.view.insert(edit, pos.begin(), c.formatmonth(2013,9+i))
			i = i + 1;
