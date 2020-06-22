db.createCollection("bots")
db.createCollection("my_bots")
db.createCollection("project")
db.createCollection("scan")
db.createCollection("scan_data")
db.createCollection("user")

db.bots.insertMany([
{
	"name" : "nobita",
	"description" : "This bot scans the ports on the specific host.",
	"created": ISODate()
},
{
	"name" : "shizuka",
	"description" : "This bot does ipreverse about a host.",
	"created": ISODate()
},
{
	"name" : "suneo",
	"description" : "This bot extract the used technologies and the CMS",
	"created": ISODate()
},
{
	"name" : "gigante",
	"description" : "This bot detects if the targets we are going to analyze have any limitations or blocking of IPs of access attempts in SSH",
	"created": ISODate()
},
])