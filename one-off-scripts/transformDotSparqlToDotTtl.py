import os
import glob

# Path to sparql files
sparql_files_path = '../scholia/app/templates/*sparql'

# Get the list of .sparql files
sparql_files = glob.glob(sparql_files_path)

aspects = {
    "author": [ "Q97270" ],
    "chemical": [ "Q2270" ],
    "publisher": [ "Q73820" ],
    "venue": [ "Q6294930" ],
    "work": [ "Q28942417" ]
}

# Process each sparql file
for i in sparql_files:
    # Extract the filename (fn) and create .ttl filename
    fn = os.path.basename(i)[0:-7]  # extract name without extension
    ttl = i[0:-7] + ".ttl"  # create .ttl filename
    aspect = fn.split("_")[0]

    # Open .ttl file to write
    with open(ttl, 'w') as ttl_file:
        ttl_file.write("""@prefix q: <https://github.com/WDScholia/scholia/scholia/app/templates/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <https://schema.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix scholia: <http://scholia.toolforge.org/ns/> .
@prefix scholiaAspect: <http://scholia.toolforge.org/ns/aspect/> .
#@prefix scholiaView: <http://scholia.toolforge.org/ns/view/> .
""")
        ttl_file.write(f"q:{fn} a sh:SPARQLExecutable,\n")

        # Read the content of the .sparql file
        with open(i, 'r') as sparql_file:
            sparql_content = sparql_file.read()

        # Check for keywords and write corresponding content
        if "SELECT" in sparql_content.upper():
            ttl_file.write("  sh:SPARQLSelectExecutable;\n")
            ttl_file.write("  sh:select '''")
        elif "CONSTRUCT" in sparql_content.upper():
            ttl_file.write("  sh:SPARQLConstructExecutable;\n")
            ttl_file.write("  sh:construct '''")
        elif "ASK" in sparql_content.upper():
            ttl_file.write("  sh:SPARQLAskExecutable ;\n")
            ttl_file.write("  sh:ask '''")
        else:
            ttl_file.write("  spex:SPARQLDescribeExecutable ;\n")
            ttl_file.write("  spex:describe '''")

        # Append sparql content to the .ttl file
        ttl_file.write(sparql_content)
        ttl_file.write("''';\n")

        # Find a title
        lines = sparql_content.splitlines()
        for line in lines:
            if line.startswith("# title:"):
                ttl_file.write("  dcterms:title \"" + line[8:].strip() + "\" ;\n")
            #if line.startswith("#defaultView:"):
            #    ttl_file.write("  scholia:defaultView scholiaView:" + line.split(":")[1] + " ;\n")

        # Add aspect info
        if aspect in aspects.keys():
            aspectClass = aspect[0].upper() + aspect[1:]
            ttl_file.write(f"  scholia:aspect scholiaAspect:{aspectClass} ;\n")
            for example in aspects[aspect]:
                ttl_file.write(f"  scholia:aspectExample wd:{example} ;\n")

        # Add the SPARQL endpoint
        ttl_file.write("  schema:target <https://query.wikidata.org/sparql> ;\n")

        # Add the license
        ttl_file.write("  dcterms:license <https://www.gnu.org/licenses/gpl-3.0> .\n")

    # Output the ttl filename
    print(ttl)
