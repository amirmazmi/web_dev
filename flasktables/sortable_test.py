from flask_table import Table, Col, LinkCol
from flask import Flask, Markup, request, url_for, render_template
import pandas as pd

"""
A example for creating a Table that is sortable by its header
"""

app = Flask(__name__)
csvfile = 'data.csv'

class SortableTable(Table):
    sitename = Col( 'Site Name' )
    address = Col( 'Address' )
    lastresp = Col( 'Last responded' )
    lastattempt = Col( 'Last Attempted')
    packetratio = Col(' Success/Sent')

    #link = LinkCol( 'Link', 'flask_link', url_kwargs=dict(id='sitename'), allow_sort=False)
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
    return render_template('results.html', table=table)

@app.route('/item/<int:id>')
def flask_link(id):
    element = Item.get_element_by_id(id)
    return '<h1>{}</h1><p>{}</p><hr><small>id: {}</small>'.format(
        element.name, element.description, element.id)


class Item(object):
    """ a little fake database """
    def __init__(self, dictdata):
        self.sitename = dictdata['sitename']
        self.address = dictdata['address']
        self.lastresp = dictdata['lastresp']
        self.lastattempt = dictdata['lastattempt']	
        self.packetratio = dictdata['packetratio']	

    @classmethod
    def get_elements(cls):
        indata = pd.read_csv(csvfile, parse_dates=[2,3])
        return [ Item( x) for x in indata.to_dict('records') ]

    @classmethod
    def get_sorted_by(cls, sort, reverse=False):
        return sorted(
            cls.get_elements(),
            key=lambda x: getattr(x, sort),
            reverse=reverse)

    @classmethod
    def get_element_by_id(cls, address):
        return [i for i in cls.get_elements() if i.address == address][0]

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)




