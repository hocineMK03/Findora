from Tokinisation import Tokinisation  # Example import
from Bigramisation import Bigramisation
from BigGramAlgo import BigGramAlgo
from TFIDF import TFIDF
from create_inverse_file import create_inverse_file
from create_connaissance_table import create_connaissance_table
from update_inverse_file import update_inverse_file
import time

from scripttodb import putdocstomongo


def performBiGram():
    # Start timing
    start_time = time.perf_counter()

    # Step 1: Tokenisation
    print("Step 1: Starting tokenisation...")
    Tokinisation().retrieve_text_files()
    after_tok_time = time.perf_counter()
    print("Step 1: Tokenisation completed.")

    # Step 2: Bigramisation
    print("Step 2: Starting bigram process...")
    Bigramisation().processDocuments()
    after_bigram_time = time.perf_counter()
    print("Step 2: Bigram process completed.")

    # Step 3: Bigram Algorithm
    print("Step 3: Starting bigram algorithm...")
    BigGramAlgo().retrieveRacines()
    after_bigram_algo_time = time.perf_counter()
    print("Step 3: Bigram algorithm completed.")

    # Step 4: TF-IDF Calculation
    print("Step 4: Calculating TF-IDF...")
    TFIDF().processTFIDFTable()
    after_tfidf_time = time.perf_counter()
    print("Step 4: TF-IDF calculation completed.")

    # Step 5: Creating connaissance and inverse tables
    print("Step 5: Creating connaissance table...")
    create_connaissance_table()
    print("Step 5: Connaissance table created.")

    print("Step 6: Creating inverse file...")
    create_inverse_file()
    print("Step 6: Inverse file created.")

    print("Step 7: Updating inverse file...")
    update_inverse_file()
    after_mongodb_time = time.perf_counter()
    print("Step 7: Inverse file updated in MongoDB.")

    # End timing
    end_time = time.perf_counter()

    # Logging time for each step
    print("\n--- Execution Time ---")
    print(f"1. Tokenisation time: {after_tok_time - start_time:.2f} seconds")
    print(f"2. Bigram process time: {after_bigram_time - after_tok_time:.2f} seconds")
    print(f"3. Bigram algorithm time: {after_bigram_algo_time - after_bigram_time:.2f} seconds")
    print(f"4. TF-IDF calculation time: {after_tfidf_time - after_bigram_algo_time:.2f} seconds")
    print(f"5-7. MongoDB operations time: {after_mongodb_time - after_tfidf_time:.2f} seconds")
    print(f"Total execution time: {end_time - start_time:.2f} seconds")
    
    putdocstomongo()
    print("Documents inserted into MongoDB.")
    print("--- End of Process ---")
performBiGram()
