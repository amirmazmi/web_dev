from flask_table import Table, Col, LinkCol
from flask import Flask, Markup, request, url_for, render_template
import pandas as pd

#------------------------------------------------------------------------------------------------------------------------------------
#
#	Alternative example from pandas
# 	https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html#Extensibility
#
#	output a html:
#		df.style.render()
#
#
#	Another alternative
#	https://sarahleejane.github.io/learning/python/2015/08/09/simple-tables-in-webapps-using-flask-and-pandas-with-python.html
#------------------------------------------------------------------------------------------------------------------------------------

"""
A example for creating a Table that is sortable by its header
"""

app = Flask(__name__)
csvfile = 'data.csv'

class SortableTable(Table):
    sitename = Col( 'Site Name', td_html_attrs={'align': 'center'} )
    address = Col( 'Address', td_html_attrs={'align': 'center'} )
    lastresp = Col( 'Last responded', td_html_attrs={'align': 'center'} )
    lastattempt = Col( 'Last Attempted', td_html_attrs={'align': 'center'} )
    packetratio = Col(' Success/Sent', td_html_attrs={'align': 'center'} )

    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('index', sort=col_key, direction=direction)


@app.route('/')
def index():
    sort = request.args.get('sort', 'address')
    reverse = (request.args.get('direction', 'asc') == 'desc')
    table = SortableTable(Item.get_sorted_by(sort, reverse),
                          sort_by=sort,
                          sort_reverse=reverse)
    #return table.__html__()
    table.border = True
    return render_template('results.html', table=table)


class Item(object):
    """ a little fake database """
    def __init__(self, dictdata):
        self.sitename = dictdata['sitename']
        self.address = dictdata['address']
        self.lastresp = dictdata['lastresp']
        self.lastattempt = dictdata['lastattempt']	
        self.packetratio = dictdata['packetratio']	

    # here just need to get data in
    @classmethod
    def get_elements(cls):
        indata = pd.read_csv(csvfile, parse_dates=[2,3])
        return indata

    # sort before handing over to table
    @classmethod
    def get_sorted_by(cls, sort, reverse=False):
        dfin = cls.get_elements()        
        # dfin = cls.get_elements().sort_values( sort, ascending=reverse)        
        # need a function to sort based on columns - address, packetratio

        if sort == 'packetratio':
            dfin['numpacketratio'] = [ eval(x) for x in dfin.packetratio]
            dfout = dfin.sort_values('numpacketratio', ascending=reverse).iloc[ :, :-1]

        elif sort == 'address':
            dfin['intaddr'] = dfin['address'].map(lambda x:tuple( int(part) for part in x.split('.') ))
            dfout = dfin.sort_values('intaddr', ascending=reverse).iloc[ :, :-1]

        else:
            dfout = dfin.sort_values(sort, ascending=reverse)

        return [ Item( x) for x in dfout.to_dict('records') ]
        


    @classmethod
    def get_element_by_id(cls, address):
        return [i for i in cls.get_elements() if i.address == address][0]

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



