from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO
import sqlite3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("query_file", help="create database with blast results of queries from query_file")
parser.add_argument("output_db_name", help="save result in output_db_name")
args = parser.parse_args()

try:
    connection = sqlite3.connect(args.output_db_name)
    c = connection.cursor()

    # Create empty tables
    with open('create_tables.sql', 'r') as f:
        create_tables_script = f.read()
    c.executescript(create_tables_script)

    # Blast queries and fill up tables
    for query in SeqIO.parse(args.query_file, format='fasta'):
        c.execute('INSERT INTO sequence (sequence_data, description) '
                  'VALUES (?, ?)', (str(query.seq), query.description))
        inserted_sequence_id = c.lastrowid
        blast_response = NCBIWWW.qblast("blastn", "nr", query.seq)
        for blast_record in NCBIXML.parse(blast_response):
            for alignment in blast_record.alignments:
                c.execute('INSERT INTO alignment (sequence_id, description) '
                          'VALUES (?, ?)', (inserted_sequence_id, alignment.title))
                inserted_alignment_id = c.lastrowid
                for hsp in alignment.hsps:
                    c.execute('INSERT INTO hit (alignment_id, percent_identity, score, e_value, align_length) '
                              'VALUES (?, ?, ?, ?, ?)',
                              (inserted_alignment_id, hsp.identities, hsp.score, hsp.expect, hsp.align_length))

    connection.commit()
except sqlite3.Error as e:
    print("Database error:", e)
except Exception as e:
    print("Query error:", e)
finally:
    if connection:
        connection.close()