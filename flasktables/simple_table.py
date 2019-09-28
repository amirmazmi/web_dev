#!/bin/python3

#-------------------------------------------------------------------------------------------------------------------------
#	http://www.blog.pythonlibrary.org/2017/12/14/flask-101-adding-editing-and-displaying-data/
#	https://flask-table.readthedocs.io/en/stable/#flask-table
#
#-------------------------------------------------------------------------------------------------------------------------
#	Script to create a html table
#		requires a template html placed in a folder called 'templates'
#
#-------------------------------------------------------------------------------------------------------------------------
from flask import Flask, flash, render_template, request, redirect
from flask_table import Table, Col
import pandas as pd 

#-------------------------------------------------------------------------------------------------------------------------

app = Flask(__name__)
csvfile = 'data.csv'
	
class Results(Table):
#	def __init__(self, csvfile):
#		self.colheaders = pd.read_csv(csvfile, parse_dates=True, nrows=2)

	sitename = Col( 'Site Name' )
	address = Col( 'Address' )
	lastresp = Col( 'Last responded' )
	lastattempt = Col( 'Last Attempted')
	packetratio = Col(' Success/Sent')

class Item(object):
	def __init__(self, sitename, address, lastresp, lastattempt, packetratio):
		self.name = name
		self.address = address
		self.lastresp = lastresp
		self.lastattempt = lastattempt	
		self.packetratio = packetratio	


@app.route('/results')
def table_results():
	results = pd.read_csv(csvfile, parse_dates=True)
	#print("\n\n", results, "\n\n")
	
	if results.shape[0] < 1:
		flash('No results found!')
		return redirect('/')
	else:
		# populate table
		items = results.to_dict('records')
		#print("\n\n", items, "\n\n")
		table = Results( items )
		#print( table.__html__() )
		
		table.border = True
		return render_template('results.html', table=table)



if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)
