import os
import glob
from rdflib import Graph

# Path to Turtle files
ttl_files_path = '../scholia/app/templates/*ttl'

# Get the list of .ttl files
ttl_files = glob.glob(ttl_files_path)

with open("scholia.json", 'w') as json_file:
    json_file.write("{\n")
    json_file.write("  \"domain\": \"scholia.toolforge.org\",\n")
    json_file.write("  \"namespace\": \"named_queries\",\n")
    json_file.write("  \"target_graph_name\": \"wikidata\",\n")
    json_file.write("  \"queries\": [\n")

    g = Graph()

    # Process each sparql file
    for i in ttl_files:
        # Extract the filename (fn) and create .sparql filename
        fn = os.path.basename(i)[0:-4]  # extract name without extension
        sparql = i[0:-4] + ".sparql"  # create .sparql filename

        g.parse(i)

    knows_query = """prefix sh: <http://www.w3.org/ns/shacl#>
prefix dcterms: <http://purl.org/dc/terms/>

SELECT DISTINCT ?query ?title ?sparql
WHERE {
    ?query sh:select | sh:ask | sh:construct ?sparql .
    OPTIONAL { ?query dcterms:title ?title }
}
ORDER BY ASC(?query)
"""

    qres = g.query(knows_query)
    for row in qres:
        queryID = row.query.replace("https://github.com/WDScholia/scholia/scholia/app/templates/", "")
        # prepare the SPARQL
        sparqlVal = row.sparql.replace("\\", "\\\\\\\\").replace("\n", "\\n").replace("\"", "\\\"").replace("\t", "\\t")

        # output the results for this SPARQL
        json_file.write("    {\n")
        json_file.write(f"      \"query_id\": \"{queryID}--named_queries@scholia.toolforge.org\",\n")
        json_file.write("      \"domain\": \"scholia.toolforge.org\",\n")
        json_file.write("      \"namespace\": \"named_queries\",\n")
        json_file.write(f"      \"name\": \"{queryID}\",\n")
        json_file.write(f"      \"sparql\": \"{sparqlVal}\",\n")
        json_file.write(f"      \"url\": \"https://raw.githubusercontent.com/WDscholia/scholia/master/scholia/app/templates/{queryID}.sparql\",\n")
        if (row.title):
            json_file.write(f"      \"title\": \"{row.title}\",\n")
        else:
            json_file.write(f"      \"title\": \"{queryID}\",\n")
        json_file.write(f"      \"description\": \"{queryID}\",\n")
        json_file.write("      \"comment\": \"\"\n")
        json_file.write("    },\n")

    json_file.write("  ]\n")
    json_file.write("}\n")
