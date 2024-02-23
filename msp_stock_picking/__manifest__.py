{
	"name": "msp_stock_picking",
	"version": "1.0", 
	"depends": [
		"base",
		"stock",
		"delivery",
	],
	"author": "asrent345@gmail.com", 
	"category": "Education", 
	'website': 'http://www.vitraining.com',
	"description": """\

Manage
======================================================================

* this is my academic information system module
* created menu:
* created object
* created views
* logic:

""",
	"data": [
		"view/marel_in_stock_picking.xml",
		"view/ir_sequence.xml",
		# "report/marel_report_menu.xml",
		# "report/report_marel_report_terima_barang_doc.xml",
		# "report/report_marel_report_pengantar_barang_doc.xml",
		# "report/report_stockpicking_barcode.xml",
		"view/report_templates.xml"
	],
	"installable": True,
	"auto_install": False,
    "application": True,
}