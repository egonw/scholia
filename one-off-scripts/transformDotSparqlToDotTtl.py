import os
import glob
import re

# Path to sparql files
sparql_files_path = '../scholia/app/templates/*sparql'

# Get the list of .sparql files
sparql_files = glob.glob(sparql_files_path)
sparql_files.sort()

aspects = {
    "author": [ "Q97270" ],
    "award": [ "Q44585" ],
    "catalogue": [ "Q51467536" ],
    "clinical-trial": [ "Q64651365" ],
    "chemical": [ "Q2270" ],
    "chemical-class": [ "Q46995757" ],
    "chemical-element": [ "Q1098" ],
    "complex": [ "Q90012272" ],
    "country": [ "Q35" ],
    "dataset": [ "Q4203254" ],
    "disease": [ "Q917357" ],
    "event": [ "Q133457282" ],
    "event-series": [ "Q47501052" ],
    "gene": [ "Q14860818" ],
    "language": [ "Q9027" ],
    "license": [ "Q20007257" ],
    "location": [ "Q1309" ],
    "ontology": [ "Q116446479" ],
    "organization": [ "Q104785223" ],
    "pathway": [ "Q28031254" ],
    "podcast": [ "Q124262264" ],
    "podcast-episode": [ "Q124268563" ],
    "podcast-language": [ "Q7411" ],
    "podcast-season": [ "Q124266519" ],
    "printer": [ "Q85200459" ],
    "project": [ "Q27990087" ],
    "property": [ "P2860" ],
    "protein": [ "Q21109365" ],
    "publisher": [ "Q73820" ],
    "software": [ "Q1635410" ],
    "sponsor": [ "Q1200258" ],
    "taxon": [ "Q12024" ],
    "topic": [ "Q45340488" ],
    "use": [ "Q1769726" ],
    "venue": [ "Q6294930" ],
    "wikiproject": [ "Q60687720" ],
    "work": [ "Q28942417" ]
}

ignore_aspects = [
    "404-chemical", "ask", "author-use", "authors", "cito", "countries", 
    "lexeme", "organizations", "series", "topics", "uses", "venues",
    "work-cito-intention", "works"
]

# Process each sparql file
number = 0
for i in sparql_files:
    print(i)
    # Extract the filename (fn) and create .ttl filename
    fn = os.path.basename(i)[0:-7]  # extract name without extension
    aspect = fn.split("_")[0]
    
    if (aspect in ignore_aspects) or aspect.endswith("-curation") or aspect.endswith("-index"):
        print(f"Ignoring aspect: {aspect}")
    elif aspect.endswith("-topic") or aspect.endswith("-use") or aspect.endswith("-statistics"):
        print(f"Ignoring aspect: {aspect}")
    elif not(aspect in aspects.keys()):
        print(f"Unsupported aspect: {aspect}")
    else:
        number = number + 1
        ttl = f"{number:03d}"+ ".ttl"  # create .ttl filename

        # Open .ttl file to write
        with open(ttl, 'w') as ttl_file:
            ttl_file.write("""@prefix q: <https://bigcat-um.github.io/sparql-examples/Scholia/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <https://schema.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix scholia: <http://scholia.toolforge.org/ns/> .
@prefix scholiaAspect: <http://scholia.toolforge.org/ns/aspect/> .
@prefix scholiaView: <http://scholia.toolforge.org/ns/view/> .
@prefix wd: <http://wikidata.org/entity/> .
@prefix wdt: <http://www.wikidata.org/prop/direct/> .
@prefix spex: <https://purl.expasy.org/sparql-examples/ontology#> .
@prefix wikibase: <http://wikiba.se/ontology#> .
@prefix cito: <http://purl.org/spar/cito/> .

""")
            ttl_file.write(f"q:{number:03d} a sh:SPARQLExecutable,\n")

            # Read the content of the .sparql file
            with open(i, 'r') as sparql_file:
                sparql_content = sparql_file.read()

            # use a specific example 
            sparql_content = sparql_content.replace("{{ q", "{{q")
            sparql_content = sparql_content.replace("q }}", "q}}")
            sparql_content = sparql_content.replace("{{q}}", aspects[aspect][0])

            # Check for keywords and write corresponding content
            if "SELECT" in sparql_content.upper():
                ttl_file.write("  sh:SPARQLSelectExecutable;\n")
                ttl_file.write("  sh:prefixes _:sparql_examples_prefixes ;\n")
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

            # Added missing prefixes
            if ("BD:" in sparql_content.upper()) and not("PREFIX BD:" in sparql_content.upper()):
                ttl_file.write("PREFIX bd: <http://www.bigdata.com/rdf#>\n")
            if ("HINT:" in sparql_content.upper()) and not("PREFIX HINT:" in sparql_content.upper()):
                ttl_file.write("PREFIX hint: <http://www.bigdata.com/queryHints#>\n")
            if ("MWAPI:" in sparql_content.upper()) and not("PREFIX MWAPI:" in sparql_content.upper()):
                ttl_file.write("PREFIX mwapi: <>\n")
            if ("P:" in sparql_content.upper()) and not("PREFIX P:" in sparql_content.upper()):
                ttl_file.write("PREFIX p: <http://www.wikidata.org/prop/>\n")
            if ("PROV:" in sparql_content.upper()) and not("PREFIX PROV:" in sparql_content.upper()):
                ttl_file.write("PREFIX prov: <http://www.w3.org/ns/prov#>\n")
            if ("PR:" in sparql_content.upper()) and not("PREFIX PR:" in sparql_content.upper()):
                ttl_file.write("PREFIX pr: <http://www.wikidata.org/prop/reference/>\n")
            if ("PQ:" in sparql_content.upper()) and not("PREFIX PQ:" in sparql_content.upper()):
                ttl_file.write("PREFIX pq: <http://www.wikidata.org/prop/qualifier/>\n")
            if ("PS:" in sparql_content.upper()) and not("PREFIX PS:" in sparql_content.upper()):
                ttl_file.write("PREFIX ps: <http://www.wikidata.org/prop/statement/>\n")
            if ("PSV:" in sparql_content.upper()) and not("PREFIX PSV:" in sparql_content.upper()):
                ttl_file.write("PREFIX psv: <http://www.wikidata.org/prop/statement/value/>\n")
            if ("RDFS:" in sparql_content.upper()) and not("PREFIX RDFS:" in sparql_content.upper()):
                ttl_file.write("PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n")
            if ("SCHEMA:" in sparql_content.upper()) and not("PREFIX SCHEMA:" in sparql_content.upper()):
                ttl_file.write("PREFIX schema: <http://schema.org/>\n")
            if ("WDT:" in sparql_content.upper()) and not("PREFIX WDT:" in sparql_content.upper()):
                ttl_file.write("PREFIX wdt: <http://www.wikidata.org/prop/direct/>\n")
            if ("WD:" in sparql_content.upper()) and not("PREFIX WD:" in sparql_content.upper()):
                ttl_file.write("PREFIX wd: <http://wikidata.org/entity/>\n")
            if ("WIKIBASE:" in sparql_content.upper()) and not("PREFIX WIKIBASE:" in sparql_content.upper()):
                ttl_file.write("PREFIX wikibase: <http://wikiba.se/ontology#>\n")
            if ("XSD:" in sparql_content.upper()) and not("PREFIX XSD:" in sparql_content.upper()):
                ttl_file.write("PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n")

            # Append sparql content to the .ttl file
            ttl_file.write(sparql_content)
            ttl_file.write("''';\n")

            # Add aspect info
            aspectClass = aspect[0].upper() + aspect[1:]
            ttl_file.write(f"  scholia:aspect scholiaAspect:{aspectClass} ;\n")

            # Find a title
            lines = sparql_content.splitlines()
            found_title = False
            for line in lines:
                if line.startswith("# title:"):
                    ttl_file.write("  rdfs:comment \"" + aspectClass + " aspect: " + line[8:].strip() + "\"@en ;\n")
                    found_title = True
                if line.startswith("#defaultView:"):
                    ttl_file.write("  scholia:defaultView scholiaView:" + line.split(":")[1] + " ;\n")

            if not(found_title):
                ttl_file.write("  rdfs:comment \"" + aspectClass + " aspect: [no title]\"@en ;\n")

            # Add the SPARQL endpoint
            ttl_file.write("  schema:target <https://query.wikidata.org/sparql> ;\n")

            if "WIKIBASE:LABEL" in sparql_content.upper():
                ttl_file.write("  spex:federatesWith <http://wikiba.se/ontology#label> ;\n")

            ttl_file.write(f"  cito:usesMethodIn <https://github.com/WDscholia/scholia/tree/master/scholia/app/templates/{fn}.sparql> ;\n")

            # Add the license
            ttl_file.write("  dcterms:license <https://www.gnu.org/licenses/gpl-3.0> .\n")

        # Output the ttl filename
        print(ttl)
